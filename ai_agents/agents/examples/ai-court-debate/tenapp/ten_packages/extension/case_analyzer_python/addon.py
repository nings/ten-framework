from ten_runtime import Addon, register_addon_as_extension, TenEnv
from .extension import CaseAnalyzerExtension


@register_addon_as_extension("case_analyzer_python")
class CaseAnalyzerExtensionAddon(Addon):
    def on_create_instance(self, ten_env: TenEnv, name: str, context) -> None:
        ten_env.log_info(f"[CaseAnalyzerAddon] Creating extension instance: {name}")
        ten_env.on_create_instance_done(CaseAnalyzerExtension(name), context)
