from __future__ import annotations

import json
import re
from typing import TYPE_CHECKING

from lxml import html

from ..postprocess import magick_gif_pp
from .site import Site

if TYPE_CHECKING:
    from ..context import CrosspostContext
    from ..queue import FragmentQueue


YT_SCRIPT_SELECTOR = ".//script[contains(text(),'responseContext')]"


class YTCommunity(Site):
    name = "yt_community"
    pattern = re.compile(
        r"https?://(?:www\.)?youtube\.com/"
        r"(?:post/|channel/[^/]+/community\?lb=)([\w-]+)"
    )

    async def handler(self, ctx: CrosspostContext, queue: FragmentQueue, post_id: str):
        link = f"https://youtube.com/post/{post_id}"

        async with self.cog.get(link) as resp:
            root = html.document_fromstring(await resp.read(), self.cog.parser)

        if not (script := root.xpath(YT_SCRIPT_SELECTOR)):
            return False

        data = json.loads(f"{{{script[0].text.partition('{')[-1].rpartition(';')[0]}")

        # jesus christ
        tab = data["contents"]["twoColumnBrowseResultsRenderer"]["tabs"][0]
        section = tab["tabRenderer"]["content"]["sectionListRenderer"]["contents"][0]
        item = section["itemSectionRenderer"]["contents"][0]
        post = item["backstagePostThreadRenderer"]["post"]["backstagePostRenderer"]

        if not (attachment := post.get("backstageAttachment")):
            return False

        images = attachment.get("postMultiImageRenderer", {}).get("images", [])

        if not images:
            images = [attachment]
        for image in images:
            if not (renderer := image.get("backstageImageRenderer")):
                continue

            thumbs = renderer["image"]["thumbnails"]
            img: str = max(thumbs, key=lambda t: t["width"])["url"]

            ext = None
            async with self.cog.get(img, method="HEAD") as resp:
                if (disp := resp.content_disposition) and (name := disp.filename):
                    ext = name.rpartition(".")[-1]

            pp = None
            ext = ext or "jpeg"

            if ext == "webp":
                pp = magick_gif_pp
                ext = "gif"

            queue.push_file(img, filename=f"{post_id}.{ext}", postprocess=pp)

        if frags := post["contentText"].get("runs"):
            text = "".join(frag.get("text", "") for frag in frags)
            queue.push_text(f">>> {text}")
