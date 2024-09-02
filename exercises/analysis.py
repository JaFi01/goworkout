from collections import defaultdict
from .models import LevelType, Muscle,Exercise, CategoryType
from django.db.models import Q

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
                    if 6 <= exercise_set.repetitions <= 12:
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
    
    def analyze_pull_push_ratio(self):
        pull_series = 0
        push_series = 0

        for plan in self.workout_routine.plans_for_day.all():
            for exercise_set in plan.exercise_sets.all():
                exercise = exercise_set.exercise
                if exercise.force == 'pull':
                    pull_series += exercise_set.series
                elif exercise.force == 'push':
                    push_series += exercise_set.series

        total_series = pull_series + push_series
        if total_series <= 2:
            return {
                "pull_series": 0,
                "push_series": 0,
                "pull_push_ratio": 0,
                "pull_deficit": False
            }

        pull_push_ratio = pull_series / push_series if push_series > 0 else float('inf')
        pull_deficit = pull_push_ratio < 0.75
        push_deficit = pull_push_ratio > 3

        return {
            "pull_series": pull_series,
            "push_series": push_series,
            "pull_push_ratio": round(pull_push_ratio, 2),
            "pull_deficit": pull_deficit,
            "push_deficit": push_deficit
        }
    
    def analyze_compound_isolation_ratio(self):
        compound_exercises = 0
        isolation_exercises = 0

        for plan in self.workout_routine.plans_for_day.all():
            for exercise_set in plan.exercise_sets.all():
                exercise = exercise_set.exercise
                if exercise.mechanic == 'compound':
                    compound_exercises += 1
                elif exercise.mechanic == 'isolation':
                    isolation_exercises += 1

        total_exercises = compound_exercises + isolation_exercises
        if total_exercises == 0:
            return {
                "compound_exercises": 0,
                "isolation_exercises": 0,
                "total_exercises": 0,
                "is_balanced": False,
                "message": "No exercises in the routine."
            }

        is_balanced = compound_exercises > isolation_exercises
        
        if is_balanced:
            message = "Correct proportion of compound to isolation exercises."
        else:
            message = "Not enough compound exercises compared to isolation exercises. Consider adding more compound exercises."

        return {
            "compound_exercises": compound_exercises,
            "isolation_exercises": isolation_exercises,
            "total_exercises": total_exercises,
            "is_balanced": is_balanced,
            "message": message
        }
    
    def suggest_exercises_for_untrained_muscles(self):
        untrained_muscles = set(self.analyze_untrained_muscles())
        suggested_exercises = {}
        user_preferred_sport = self.workout_routine.user.preferred_sport

        for muscle in untrained_muscles:
            suggested_exercises[muscle] = []
            # Firstly we search for exercises that match user's preferred sport
            preferred_exercises = Exercise.objects.filter(
                Q(primary_muscles__contains=[muscle]) | Q(secondary_muscles__contains=[muscle]),
                category=user_preferred_sport
            ).values('name').distinct()[:3]

            for exercise in preferred_exercises:
                exercise_info = {
                    'name': exercise['name'],
                    'matches_preferred_sport': True
                }
                suggested_exercises[muscle].append(exercise_info)

            if len(suggested_exercises[muscle]) < 3:
                other_exercises = Exercise.objects.filter(
                    Q(primary_muscles__contains=[muscle]) | Q(secondary_muscles__contains=[muscle])
                ).exclude(name__in=[e['name'] for e in suggested_exercises[muscle]]).values('name').distinct()[:3 - len(suggested_exercises[muscle])]

                for exercise in other_exercises:
                    exercise_info = {
                        'name': exercise['name'],
                        'matches_preferred_sport': False
                    }
                    suggested_exercises[muscle].append(exercise_info)

        return suggested_exercises

    def get_analysis_report(self):
        trained_muscles = self.analyze_trained_muscles()
        untrained_muscles = self.analyze_untrained_muscles()
        repetition_range_check = self.check_repetition_range()
        pull_push_analysis = self.analyze_pull_push_ratio()
        compound_isolation_analysis = self.analyze_compound_isolation_ratio()
        suggested_exercises = self.suggest_exercises_for_untrained_muscles()
        return {
            
            "trained_muscles": trained_muscles,
            "untrained_muscles": untrained_muscles,
            "repetition_range_check": repetition_range_check,
            "pull_push_analysis": pull_push_analysis,
            "compound_isolation_analysis": compound_isolation_analysis,
            "suggested_exercises": suggested_exercises
        }