from collections import defaultdict
from .models import WorkoutRoutine, PlanForDay, ExerciseSet, Exercise, Muscle

class Analysis:
    def __init__(self, workout_routine):
        self.workout_routine = workout_routine
        self.all_muscle_groups = set(Muscle.values)

    def analyze_trained_muscles(self):
        muscle_stats = defaultdict(lambda: {"exercises": set(), "series": 0})
        
        for plan in self.workout_routine.plans_for_day.all():
            for exercise_set in plan.exercise_sets.all():
                exercise = exercise_set.exercise
                primary_muscles = exercise.primary_muscles or []
                secondary_muscles = exercise.secondary_muscles or []
                
                for muscle in primary_muscles + secondary_muscles:
                    muscle_stats[muscle]["exercises"].add(exercise.name)
                    muscle_stats[muscle]["series"] += exercise_set.series

        result = {}
        for muscle, stats in muscle_stats.items():
            result[muscle] = {
                "exercise_count": len(stats["exercises"]),
                "total_series": stats["series"]
            }
        
        return result

    def analyze_untrained_muscles(self):
        trained_muscles = set(self.analyze_trained_muscles().keys())
        untrained_muscles = self.all_muscle_groups - trained_muscles
        return list(untrained_muscles)

    def get_analysis_report(self):
        trained_muscles = self.analyze_trained_muscles()
        untrained_muscles = self.analyze_untrained_muscles()

        report = "Analiza planu treningowego:\n\n"
        report += "Trenowane grupy mięśniowe:\n"
        for muscle, stats in trained_muscles.items():
            report += f"- {muscle}: {stats['exercise_count']} ćwiczeń, {stats['total_series']} serii\n"
        
        report += "\nNietrenowane grupy mięśniowe:\n"
        for muscle in untrained_muscles:
            report += f"- {muscle}\n"

        return report