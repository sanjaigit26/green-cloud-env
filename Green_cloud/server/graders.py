class EasyGrader:
    def grade(self, env) -> float:
        try:
            if env is None:
                return 0.5
            jobs = getattr(env, "jobs", None) or []
            total_jobs = len(jobs)
            if total_jobs <= 0:
                return 0.5
            assigned = sum(1 for j in jobs if getattr(j, "assigned", False))
            score = assigned / total_jobs
            if score <= 0.0 or score >= 1.0:
                return 0.5
            return score
        except Exception:
            return 0.5

class MediumGrader:
    def grade(self, env) -> float:
        try:
            if env is None:
                return 0.5
            jobs = getattr(env, "jobs", None) or []
            current_time = getattr(env, "time", 0)
            total_jobs = len(jobs)
            if total_jobs <= 0:
                return 0.5
            success = sum(
                1 for j in jobs
                if getattr(j, "assigned", False)
                and current_time <= getattr(j, "deadline", current_time)
            )
            score = success / total_jobs
            if score <= 0.0 or score >= 1.0:
                return 0.5
            return score
        except Exception:
            return 0.5

class HardGrader:
    def grade(self, env) -> float:
        try:
            if env is None:
                return 0.5
            jobs = getattr(env, "jobs", None) or []
            regions = getattr(env, "regions", None) or []
            energy_sources = getattr(env, "energy_sources", None) or {}
            total_jobs = len(jobs)
            if total_jobs <= 0:
                return 0.5
            success_count = 0
            total_carbon = 0.0
            for j in jobs:
                if not getattr(j, "assigned", False):
                    continue
                assigned_region = getattr(j, "assigned_region", None)
                if not assigned_region:
                    continue
                region = next(
                    (r for r in regions if getattr(r, "name", None) == assigned_region),
                    None
                )
                if region is None:
                    continue
                energy_mix = getattr(region, "energy_mix", {}) or {}
                carbon = 0.0
                for source_name, ratio in energy_mix.items():
                    source = energy_sources.get(source_name)
                    if source is None:
                        continue
                    carbon += getattr(source, "carbon_intensity", 0.0) * float(ratio)
                success_count += 1
                total_carbon += carbon
            if success_count == 0:
                return 0.5
            completion = success_count / total_jobs
            avg_carbon = total_carbon / success_count
            carbon_score = 1.0 - avg_carbon
            weighted = 0.6 * completion + 0.4 * carbon_score
            if weighted <= 0.0 or weighted >= 1.0:
                return 0.5
            return weighted
        except Exception:
            return 0.5
