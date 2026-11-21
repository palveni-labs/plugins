# Palveni 插件

这里发布 Palveni Server 的官方皮肤，也接受社区提交的皮肤。每种皮肤都提供浅色和深色外观。

| 皮肤 | 源码 | 外观 |
| --- | --- | --- |
| 原生克制 | [skin-native](skin-native/) | 中性灰背景、海军蓝强调色和带文字的侧边栏 |
| 纸墨 | [skin-ink](skin-ink/) | 纸色背景、衬线标题和朱红色提醒 |
| 器材 | [skin-gear](skin-gear/) | 石墨色、紧凑排版和琥珀色状态标记 |

## 安装

管理员可在 Palveni 工作台的「应用 → 外观」一键安装官方皮肤。服务端会核对该版本的 SHA-256，安装后即可切换外观。官方的未压缩 tar 包可从 [Releases](https://github.com/palveni-labs/plugins/releases) 下载。社区皮肤可以在同一页面通过「上传皮肤」安装。

## 提交社区皮肤

通过 Pull Request 提交独立的皮肤目录或公开源码链接。在说明中列出插件 ID、版本、许可证、所含字体与图片的来源。如果提供下载包，请附上固定版本的下载地址和 SHA-256。

可以参考 [纸墨的清单](skin-ink/plugin.toml) 和 [皮肤定义](skin-ink/skin.json)。使用自己的插件 ID，在包的根目录放置 `plugin.toml` 和 `skin.json`。当前支持的皮肤使用 `runtime = "none"`，只含声明和静态资源，无需申请权限。上传使用未压缩的 POSIX tar，整包上限为 16 MiB。

维护者会检查资源许可、包内容、浅深色预览及实际安装效果。官方一键安装目录随服务端版本发布。

## 许可证

官方皮肤使用 [MPL-2.0](LICENSE)。字体保留各自的许可证，详见各皮肤 `fonts/` 目录下的 `LICENSE-*.txt`。
