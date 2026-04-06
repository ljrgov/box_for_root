#### 更新日志 v1.10.2 - 05-09-25
- 修复(scripts)：在 box.tool 中使用 `/system/bin/sh` 并增加 `curl` 超时选项
- 修复：在 restore_ini 的 sed 替换中转义特殊字符
- box.tool（subs）：扩展协议检测并澄清错误日志
- 新功能：支持 Base64 订阅（clash/momo）文件在 box.tool 中
- 重构(settings)：将 GID 列表移至单独的 gid.list.cfg 文件
- 增加恢复和应用 settings.ini 功能
- box：将 sing-box 切换为单个配置文件

#### 更新日志 v1.10.1 - 23-08-25
- 修复：在网络切换过程中改进 SSID 获取准确性（网络控制）