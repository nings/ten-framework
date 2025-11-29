from ten_runtime import Addon, register_addon_as_extension, TenEnv
from .extension import LegalKnowledgeExtension


@register_addon_as_extension("legal_knowledge_python")
class LegalKnowledgeExtensionAddon(Addon):
    def on_create_instance(self, ten_env: TenEnv, name: str, context) -> None:
        ten_env.log_info(f"[LegalKnowledgeAddon] Creating extension instance: {name}")
        ten_env.on_create_instance_done(LegalKnowledgeExtension(name), context)
