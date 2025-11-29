"""
LLM Integration Module – Generates natural language insights using OpenAI or fallback mock logic.
"""

import os
from typing import Dict, Any


class LLMInsightGenerator:
    """Generates personalized natural language insights using an LLM."""

    def __init__(self, api_key: str = None, use_mock: bool = False):
        self.use_mock = use_mock
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")

        if not self.use_mock and not self.api_key:
            self.use_mock = True

        if not self.use_mock:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=self.api_key)
            except ImportError:
                self.use_mock = True

    def generate_insight(self, analysis_result: Dict[str, Any], user_data: Dict[str, Any]) -> str:
        if self.use_mock:
            return self._generate_mock_insight(analysis_result, user_data)

        try:
            return self._generate_openai_insight(analysis_result, user_data)
        except Exception:
            return self._generate_mock_insight(analysis_result, user_data)

    def _generate_openai_insight(self, analysis_result: Dict[str, Any], user_data: Dict[str, Any]) -> str:
        prompt = self._build_prompt(analysis_result, user_data)

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a digital wellness coach providing personalized, concise insights "
                        "about screen time and app usage. Keep responses to 3–4 sentences with one "
                        "clear recommendation."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=200,
        )

        return response.choices[0].message.content.strip()

    def _generate_mock_insight(self, analysis_result: Dict[str, Any], user_data: Dict[str, Any]) -> str:
        score = analysis_result["overall_score"]
        tags = analysis_result["tags"]
        hours = analysis_result["metrics"]["total_screen_time_hours"]

        if score >= 80:
            opening = f"Your wellness score of {score}/100 reflects strong digital habits."
        elif score >= 60:
            opening = f"Your wellness score of {score}/100 indicates generally balanced usage with areas to refine."
        else:
            opening = f"Your wellness score of {score}/100 suggests several patterns worth addressing."

        observations = []

        if "night-owl" in tags:
            observations.append("Late-night screen time may be affecting sleep quality")

        if "workaholic" in tags or "heavy-user" in tags:
            observations.append(f"Your daily usage of {hours} hours may benefit from clearer boundaries")

        if "marathon-sessions" in tags:
            observations.append("Long sessions without breaks can contribute to fatigue")

        if "social-butterfly" in tags:
            observations.append("High social media usage was detected")

        if "balanced" in tags:
            observations.append("Your overall app usage balance is healthy")

        recommendations = []
        breakdown = analysis_result["breakdown"]

        if score < 70:
            if breakdown["timing"] < 60:
                recommendations.append("Try reducing screen exposure one hour before bedtime")
            if breakdown["breaks"] < 60:
                recommendations.append("Use the 20-20-20 rule to reduce eye strain")
            if hours > 8:
                recommendations.append("Consider setting daily screen time limits")

        parts = [opening]

        if observations:
            parts.append(f"{observations[0]}.")

        if recommendations:
            parts.append(f"Recommendation: {recommendations[0]}.")

        return " ".join(parts)

    def _build_prompt(self, analysis_result: Dict[str, Any], user_data: Dict[str, Any]) -> str:
        score = analysis_result["overall_score"]
        breakdown = analysis_result["breakdown"]
        tags = ", ".join(analysis_result["tags"])
        patterns = "; ".join(analysis_result["patterns"]) if analysis_result["patterns"] else "None"
        hours = analysis_result["metrics"]["total_screen_time_hours"]

        return f"""
Analyze this digital wellness data and provide a concise, personalized insight.

Overall Wellness Score: {score}/100
Screen Time: {hours} hours
Behavioral Tags: {tags}
Patterns Detected: {patterns}

Score Breakdown:
- Screen Time: {breakdown['screen_time']}/100
- App Diversity: {breakdown['diversity']}/100
- Usage Timing: {breakdown['timing']}/100
- Category Balance: {breakdown['balance']}/100
- Break Patterns: {breakdown['breaks']}/100

Provide a 3–4 sentence insight that:
1. Acknowledges their current wellness level
2. Highlights the most important behavioral pattern
3. Offers one specific, actionable recommendation
""".strip()
