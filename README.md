# DeepSearch CLI

这是一个专用的命令行客户端 (CLI client)，用于连接和交互私有的 `deep-search` 服务。

> **⚠️ 重要提示**
>
> 本项目**仅作为客户端**，极度依赖于**非公开的 `deep-search` 后端服务**，因此**无法**作为独立的本地搜索工具单独使用。如果您没有该后端服务的访问权限及配置环境，此客户端将无法工作。

## 快速安装

您可以直接通过以下命令，从公网方便地安装或更新 `deep-search` 客户端：

```bash
curl -sSL https://raw.githubusercontent.com/radiumce/deep-search-cli/main/scripts/install-cli.sh | bash
```

安装脚本会自动由 GitHub 拉取最新的 `deep-search` 客户端程序，并安装到您系统用户的 `~/.local/bin` 目录下。

*(注：安装完成后，请确保您的系统 `PATH` 环境变量中包含 `~/.local/bin`)*

## 配置与使用

在使用前，您需要先指定您的私有服务地址：

```bash
deep-search --server <YOUR_PRIVATE_SERVER_URL>
```

### 基础指令

- **智能搜索 (Search):**
  ```bash
  deep-search search "您的搜索问题"
  ```

- **网页提取 (Browse):**
  ```bash
  deep-search browse "https://example.com"
  ```

- **检查当前配置与服务器健康状态:**
  ```bash
  deep-search
  ```
