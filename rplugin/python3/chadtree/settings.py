from typing import Any

from .consts import colours_json, config_json, icons_json, ignore_json, view_json
from .da import load_json, merge
from .highlight import gen_hl
from .ls_colours import parse_ls_colours
from .types import Settings, UpdateTime, VersionControlOptions, ViewOptions


def initial(user_config: Any, user_view: Any, user_ignores: Any) -> Settings:
    config = merge(load_json(config_json), user_config)
    view = merge(load_json(view_json), user_view)
    icon_c = load_json(icons_json)
    ignore = merge(load_json(ignore_json), user_ignores)
    colours = load_json(colours_json)

    use_icons = config["use_icons"]
    view_c = view["unicode"] if use_icons else view["ascii"]

    ext_colours = gen_hl("github", mapping=colours)
    icons = ViewOptions(
        active=view_c["status"]["active"],
        default_icon=view_c["default_icon"],
        folder_closed=view_c["folder"]["closed"],
        folder_open=view_c["folder"]["open"],
        link=view_c["link"]["normal"],
        link_broken=view_c["link"]["broken"],
        selected=view_c["status"]["selected"],
        quickfix_hl=view["highlights"]["quickfix"],
        version_ctl_hl=view["highlights"]["version_control"],
        ext_colours=ext_colours,
        filename_exact=icon_c["name_exact"],
        filename_glob=icon_c["name_glob"],
        filetype=icon_c["type"],
    )

    update = UpdateTime(
        min_time=config["update_time"]["min"], max_time=config["update_time"]["max"]
    )

    version_ctl = VersionControlOptions(defer=config["version_control"]["defer"])
    hl_context = parse_ls_colours()

    keymap = {f"CHAD{k}": v for k, v in config["keymap"].items()}

    settings = Settings(
        follow=config["follow"],
        icons=icons,
        hl_context=hl_context,
        keymap=keymap,
        name_ignore=ignore["name"],
        open_left=config["open_left"],
        path_ignore=ignore["path"],
        session=config["session"],
        show_hidden=config["show_hidden"],
        update=update,
        use_icons=use_icons,
        version_ctl=version_ctl,
        width=config["width"],
    )

    return settings
