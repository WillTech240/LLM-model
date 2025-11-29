"""
Test script for Digital Wellness Analyzer.
Runs the analyzer and LLM integration without the web interface.
"""

from analyzer import WellnessAnalyzer
from llm_insights import LLMInsightGenerator
import json

# Sample test data
test_data = {
    "date": "2025-11-28",
    "total_screen_time_minutes": 540,
    "apps": [
        {"name": "VS Code", "category": "productivity", "minutes": 240},
        {"name": "Chrome", "category": "productivity", "minutes": 120},
        {"name": "Instagram", "category": "social", "minutes": 90},
        {"name": "YouTube", "category": "entertainment", "minutes": 60},
        {"name": "Slack", "category": "productivity", "minutes": 30}
    ],
    "sessions": [
        {"start_hour": 9, "end_hour": 12, "minutes": 180},
        {"start_hour": 14, "end_hour": 18, "minutes": 240},
        {"start_hour": 22, "end_hour": 23, "minutes": 60}
    ]
}

print("=" * 60)
print("DIGITAL WELLNESS ANALYZER - TEST")
print("=" * 60)
print()

# Initialize components
print("Initializing analyzer and LLM generator...")
analyzer = WellnessAnalyzer()
llm_generator = LLMInsightGenerator(use_mock=True)
print("Initialization complete.")
print()

# Run analysis
print("Running analysis on sample data...")
result = analyzer.analyze(test_data)
print("Analysis complete.")
print()

# Display results
print("=" * 60)
print("ANALYSIS RESULTS")
print("=" * 60)
print()

print(f"Overall Wellness Score: {result['overall_score']}/100")
print()

print("Score Breakdown:")
for category, score in result["breakdown"].items():
    label = category.replace("_", " ").title()
    print(f"  - {label}: {score}/100")
print()

print("Behavioral Tags:")
print(", ".join(result["tags"]))
print()

print("Detected Patterns:")
for pattern in result["patterns"]:
    print(f"  - {pattern}")
print()

print("Quick Metrics:")
print(f"  - Total Screen Time: {result['metrics']['total_screen_time_hours']} hours")
print(f"  - Apps Used: {result['metrics']['app_count']}")
print(f"  - Sessions: {result['metrics']['session_count']}")
print()

# LLM Insight
print("=" * 60)
print("LLM INSIGHT")
print("=" * 60)
print()

insight = llm_generator.generate_insight(result, test_data)
print(insight)
print()

print("=" * 60)
print("TEST COMPLETED")
print("=" * 60)
