"""
Digital Wellness Analyzer - Rule-based Intelligence Engine
Analyzes screen time and app usage patterns to generate wellness scores and behavioral tags.
"""

from typing import Dict, List, Any


class WellnessAnalyzer:
    """Core rule-based engine for analyzing digital wellness patterns."""
    
    def __init__(self):
        self.max_score = 100
        
    def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        total_screen_time = data.get("total_screen_time_minutes", 0)
        apps = data.get("apps", [])
        sessions = data.get("sessions", [])

        screen_time_score = self._score_screen_time(total_screen_time)
        diversity_score = self._score_app_diversity(apps)
        timing_score = self._score_usage_timing(sessions)
        balance_score = self._score_category_balance(apps)
        break_score = self._score_breaks(sessions)

        overall_score = self._calculate_overall_score({
            "screen_time": screen_time_score,
            "diversity": diversity_score,
            "timing": timing_score,
            "balance": balance_score,
            "breaks": break_score
        })
        
        tags = self._generate_tags(data, overall_score, {
            "screen_time": screen_time_score,
            "diversity": diversity_score,
            "timing": timing_score,
            "balance": balance_score,
            "breaks": break_score
        })
        
        patterns = self._identify_patterns(data, apps, sessions)
        
        return {
            "overall_score": round(overall_score, 1),
            "breakdown": {
                "screen_time": round(screen_time_score, 1),
                "diversity": round(diversity_score, 1),
                "timing": round(timing_score, 1),
                "balance": round(balance_score, 1),
                "breaks": round(break_score, 1)
            },
            "tags": tags,
            "patterns": patterns,
            "metrics": {
                "total_screen_time_hours": round(total_screen_time / 60, 1),
                "app_count": len(apps),
                "session_count": len(sessions)
            }
        }
    
    def _score_screen_time(self, minutes: int) -> float:
        hours = minutes / 60
        if hours <= 4: return 100
        if hours <= 6: return 85
        if hours <= 8: return 70
        if hours <= 10: return 50
        if hours <= 12: return 30
        return 10
    
    def _score_app_diversity(self, apps: List[Dict]) -> float:
        if not apps:
            return 50
        count = len(apps)
        if 4 <= count <= 8: return 100
        if 2 <= count <= 10: return 80
        if count == 1: return 40
        return 60
    
    def _score_usage_timing(self, sessions: List[Dict]) -> float:
        if not sessions:
            return 50
        
        late_night = 0
        early_morning = 0
        
        for s in sessions:
            start = s.get("start_hour", 0)
            end = s.get("end_hour", 0)
            duration = s.get("minutes", (end - start) * 60)

            if start >= 23 or end >= 23 or start <= 2 or end <= 2:
                late_night += duration
            if 5 <= start <= 7 or 5 <= end <= 7:
                early_morning += duration
        
        score = 100
        
        if late_night > 120: score -= 40
        elif late_night > 60: score -= 25
        elif late_night > 30: score -= 15
        
        if early_morning > 60:
            score -= 10
        
        return max(0, score)
    
    def _score_category_balance(self, apps: List[Dict]) -> float:
        if not apps:
            return 50
        
        category_minutes = {}
        total = 0
        
        for app in apps:
            cat = app.get("category", "other")
            mins = app.get("minutes", 0)
            category_minutes[cat] = category_minutes.get(cat, 0) + mins
            total += mins
        
        if total == 0:
            return 50
        
        percentages = {c: (m / total) * 100 for c, m in category_minutes.items()}
        score = 100
        
        dominant = max(percentages.values())
        if dominant > 70: score -= 30
        elif dominant > 60: score -= 15
        
        productivity = percentages.get("productivity", 0)
        if 30 <= productivity <= 60:
            score += 10
        
        social = percentages.get("social", 0)
        if social > 40: score -= 20
        elif social > 30: score -= 10
        
        return max(0, min(100, score))
    
    def _score_breaks(self, sessions: List[Dict]) -> float:
        if len(sessions) <= 1:
            return 60
        
        sorted_sessions = sorted(sessions, key=lambda x: x.get("start_hour", 0))
        breaks = []

        for i in range(len(sorted_sessions) - 1):
            end_current = sorted_sessions[i].get("end_hour", 0)
            start_next = sorted_sessions[i + 1].get("start_hour", 0)
            duration = start_next - end_current
            if duration > 0:
                breaks.append(duration)

        if not breaks:
            return 40
        
        avg_break = sum(breaks) / len(breaks)

        if 1 <= avg_break <= 2: return 100
        if 0.5 <= avg_break <= 3: return 85
        if avg_break < 0.5: return 50
        return 70
    
    def _calculate_overall_score(self, scores: Dict[str, float]) -> float:
        weights = {
            "screen_time": 0.30,
            "diversity": 0.15,
            "timing": 0.25,
            "balance": 0.20,
            "breaks": 0.10
        }
        return sum(scores[k] * weights[k] for k in weights)
    
    def _generate_tags(self, data: Dict, overall: float, scores: Dict[str, float]) -> List[str]:
        tags = []
        total = data.get("total_screen_time_minutes", 0)
        apps = data.get("apps", [])
        sessions = data.get("sessions", [])

        if overall >= 80: tags.append("balanced")
        elif overall >= 60: tags.append("moderate")
        else: tags.append("needs-attention")
        
        hours = total / 60
        if hours > 10: tags.append("heavy-user")
        elif hours > 8: tags.append("workaholic")
        elif hours < 3: tags.append("light-user")
        
        if scores["timing"] < 60:
            tags.append("night-owl")
        
        for s in sessions:
            if s.get("start_hour", 0) <= 6:
                tags.append("early-bird")
                break
        
        category_minutes = {}
        for app in apps:
            cat = app.get("category", "other")
            category_minutes[cat] = category_minutes.get(cat, 0) + app.get("minutes", 0)
        
        if total > 0:
            productivity = (category_minutes.get("productivity", 0) / total) * 100
            social = (category_minutes.get("social", 0) / total) * 100
            
            if productivity > 50: tags.append("focused")
            if social > 40: tags.append("social-butterfly")
        
        if len(apps) <= 2: tags.append("single-minded")
        elif len(apps) >= 10: tags.append("multitasker")
        
        if scores["breaks"] >= 80: tags.append("good-breaks")
        elif scores["breaks"] < 50: tags.append("marathon-sessions")
        
        return tags
    
    def _identify_patterns(self, data: Dict, apps: List[Dict], sessions: List[Dict]) -> List[str]:
        patterns = []
        total = data.get("total_screen_time_minutes", 0)
        
        late_night = [s for s in sessions if s.get("start_hour", 0) >= 22 or s.get("end_hour", 0) >= 23]
        if late_night:
            patterns.append(f"Late night usage detected in {len(late_night)} session(s)")
        
        if apps:
            top_app = max(apps, key=lambda x: x.get("minutes", 0))
            pct = (top_app.get("minutes", 0) / total * 100) if total > 0 else 0
            if pct > 50:
                patterns.append(f"Heavy focus on {top_app.get('name', 'Unknown')} ({pct:.0f}% of time)")
        
        long_sessions = [s for s in sessions if (s.get("end_hour", 0) - s.get("start_hour", 0)) > 4]
        if long_sessions:
            patterns.append(f"{len(long_sessions)} extended session(s) over 4 hours")
        
        category_minutes = {}
        for app in apps:
            cat = app.get("category", "other")
            category_minutes[cat] = category_minutes.get(cat, 0) + app.get("minutes", 0)
        
        if total > 0 and category_minutes:
            dom = max(category_minutes.items(), key=lambda x: x[1])
            if (dom[1] / total) > 0.7:
                patterns.append(f"Heavily skewed toward {dom[0]} activities")
        
        return patterns
