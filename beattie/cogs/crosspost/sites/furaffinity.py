from __future__ import annotations

import re
from typing import TYPE_CHECKING

from lxml import html

from .site import Site
from .selectors import OG_DESCRIPTION, OG_IMAGE, OG_TITLE

if TYPE_CHECKING:
    from ..context import CrosspostContext
    from ..queue import FragmentQueue


class FurAffinity(Site):
    name = "furaffinity"
    pattern = re.compile(r"https?://(?:www\.)?(?:[fv]x)?f[ux]raffinity\.net/view/(\d+)")

    async def handler(self, ctx: CrosspostContext, queue: FragmentQueue, sub_id: str):
        link = f"https://www.fxraffinity.net/view/{sub_id}?full"
        async with self.cog.get(
            link, error_for_status=False, allow_redirects=False
        ) as resp:
            root = html.document_fromstring(await resp.read(), self.cog.parser)

        try:
            url = root.xpath(OG_IMAGE)[0].get("content")
        except IndexError:
            queue.push_text(
                "No images found. Post may be login-restricted.", force=True
            )
            return

        queue.push_file(url)

        title = root.xpath(OG_TITLE)[0].get("content")
        desc = root.xpath(OG_DESCRIPTION)[0].get("content")
        queue.push_text(f"**{title}**")
        queue.push_text(f">>> {desc}")
