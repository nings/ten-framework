from ten_runtime import Addon, register_addon_as_extension, TenEnv
from .extension import CourtDebateControlExtension


@register_addon_as_extension("court_debate_control_python")
class CourtDebateControlExtensionAddon(Addon):
    def on_create_instance(self, ten_env: TenEnv, name: str, context) -> None:
        ten_env.log_info(f"[CourtDebateControlAddon] Creating extension instance: {name}")
        ten_env.on_create_instance_done(CourtDebateControlExtension(name), context)
