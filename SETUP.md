# 个人主页文件包

`README.md` 是发布正文；`assets/` 是仓库内图片，`tools/` 是素材脚本，`.github/workflows/` 是贡献图自动生成配置。上传的是本目录里的内容，不是把 `github-profile` 文件夹整体嵌套进去。完整压缩包 `github-profile.zip` 已包含 `.github` 隐藏目录。

**先看效果：**解压后用浏览器打开 `PREVIEW.html`，可以直接播放动效；系统开启“减少动画”时展示静态版本。预览 HTML 是派生产物，改 README 后需重新生成，发布到 GitHub 并不需要上传它。

## 上传与首次启用

1. 在 GitHub 创建公开仓库 **pmsjl/pmsjl**，使用 `main` 默认分支；如果已经存在，先检查并保留原有文件，再合并本文件包。
2. 将本目录内 README、assets、tools、.gitignore、.github 等文件按原结构提交到仓库根目录。网页上传时也要包含隐藏的 `.github` 目录；也可以使用本地 Git 上传。
3. GitHub 主页会展示 README。姓名横幅、打字介绍、分隔线和页脚来自仓库内 SVG；方形联系徽章直接使用 Shields.io 的 for-the-badge 样式，访问计数使用 Komarev 的 pmsjl 计数，需要网络访问。
4. 打开仓库 **Actions → Profile visuals → Run workflow**，分支选择 `main`。首次推送工作流也会触发；重复手动运行是安全的。
5. 工作流成功后会提交四张生成图，替换“等待首次生成”提示。刷新主页即可看到 pmsjl 的公开贡献。如果 GitHub 图片缓存未刷新，稍后再次查看。

工作流每天北京时间 **04:17** 调度（UTC 20:17），实际执行可能延迟；也支持手动运行和工作流/发布脚本变更触发。默认使用内置 `GITHUB_TOKEN`，不需要提供个人访问令牌。若组织策略或分支保护禁止机器人写入，检查 Actions 运行日志和仓库策略；不要为此直接关闭保护规则。本次本地制作未创建仓库、未推送，也未启用远程调度。

## 修改内容与素材

- 正文以本目录 `README.md` 为准。上一级 `github-profile-README.md` 是同正文镜像；其图片路径按本发布包根目录解析，查看完整效果请打开本目录或交付的 HTML 预览。
- 修改素材：横幅与打字采用参考 README 同款 Capsule Render / Readme Typing SVG 输出，保存在 `tools/templates/`；编辑模板或 `tools/build_assets.py`，在本目录运行 `python tools/build_assets.py` 重新生成。只用 Python 标准库。
- 首次初始化占位图：`python tools/build_assets.py --seed-placeholders`。已有贡献图不会被覆盖。
- 动效为图片内 CSS / SVG SMIL：横幅波浪 20 秒、大标题 1.2 秒淡入；打字为 600 字重的 Fira Code，每句约 4.6 秒（含约 2 秒停留）；分隔线 8 秒、页脚 9 秒。横幅、打字、分隔线和页脚提供减少动效静态图；第三方贡献图的减少动效行为不作保证。
- 第三方图片无法生成时，远端已提交的旧图保持不变。所有新图完整生成并通过 SVG 检查后才提交；无变化不提交，不强制推送。
- 贡献城市暂不在 README 展示，素材与生成流程保留，方便以后恢复；当前贡献区仅展示贪吃蛇。
- 两个主要项目有在线演示，其他入口指向真实仓库。主页不展示未经核实的运行时长、用户量或提交数量，也不重复维护评测百分比。

## 预览与验收边界

本地 HTML 为接近 GitHub Markdown 的预览，不代表已经上线。主要内容保留原生文字、Markdown 与 GitHub 支持的基础 HTML，不使用页面脚本实现 README 动画。源码工作区的 `.verify/profile_preview.mjs` 用于生成预览与截图；它使用工作区已有的 marked、Playwright 和 Chrome，不是贡献图工作流的运行依赖。

发布后仍需检查 GitHub 实际渲染、Actions 首次运行和主题切换。首次运行前的占位图不含贡献数据。README 中三处流光分隔线和底部贡献区均可单独删去，不影响正文。

## 第三方来源

- [Capsule Render](https://github.com/kyechan99/capsule-render)：深紫渐变波浪横幅，姓名 50px / 700、副标题 18px / 700，青色 #00F7FF。
- [Readme Typing SVG](https://github.com/DenverCoder1/readme-typing-svg)：透明背景、居中青色打字，26px / 600。内嵌 Fira Code 字体许可见 `licenses/FiraCode-OFL.txt`。

- [GitHub Profile README](https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme)
- [Platane/snk](https://github.com/Platane/snk)：贡献贪吃蛇，工作流固定 v3 对应提交。
- [github-profile-3d-contrib](https://github.com/yoshi389111/github-profile-3d-contrib)：3D 贡献城市，工作流固定 2026-09-07 核实的发布提交。

贡献数据仅用于个人活动展示。第三方生成器版本升级需重新检查输出文件名和渲染结果。
