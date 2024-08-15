from collections import defaultdict
from .models import LevelType, Muscle

class Analysis:
    def __init__(self, workout_routine):
        self.workout_routine = workout_routine
        self.all_muscle_groups = set(Muscle.values)
        self.excluded_muscles = {'Forearms', 'Adductors', 'Neck', 'Abdominals'}


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
    
    def check_repetition_range(self):
        if self.workout_routine.user.fitness_level not in [LevelType.BEGINNER, LevelType.INTERMEDIATE]:
            return None  # Nie sprawdzamy dla zaawansowanych

        total_exercises = 0
        exercises_in_range = 0

        for plan in self.workout_routine.plans_for_day.all():
            for exercise_set in plan.exercise_sets.all():
                exercise = exercise_set.exercise
                if not any(muscle in self.excluded_muscles for muscle in exercise.primary_muscles + exercise.secondary_muscles):
                    total_exercises += 1
                    if 8 <= exercise_set.repetitions <= 12:
                        exercises_in_range += 1

        if total_exercises == 0:
            return 0  # No 0 division

        percentage = (exercises_in_range / total_exercises) * 100
        meets_criteria = percentage >= 50

        return {
            "total_exercises": total_exercises,
            "exercises_in_range": exercises_in_range,
            "percentage": round(percentage, 2),
            "meets_criteria": meets_criteria
        }


    def get_analysis_report(self):
        trained_muscles = self.analyze_trained_muscles()
        untrained_muscles = self.analyze_untrained_muscles()
        repetition_range_check = self.check_repetition_range()
        
        return {
            "trained_muscles": trained_muscles,
            "untrained_muscles": untrained_muscles,
            "repetition_range_check": repetition_range_check
        }