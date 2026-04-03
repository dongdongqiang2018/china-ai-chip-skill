#!/usr/bin/env node
/**
 * MCP Server: 从 https://gitcode.com/Ascend/pytorch 抓取对应 torch_npu 版本文档
 * 分支命名规则: v{PyTorch版本}-{昇腾版本}，例如 v2.7.1-7.3.0
 */

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import * as fs from "fs";
import * as path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const GITCODE_BASE = "https://gitcode.com/Ascend/pytorch";
const DEFAULT_BRANCH = "v2.7.1-7.3.0";

// 常用中文文档路径（与 reference.md 对应）
const DOC_PATHS_ZH = [
  "README.zh.md",
  "CONTRIBUTING.zh.md",
  "docs/zh/overview/product_overview.md",
  "docs/zh/quick_start/quick_start.md",
  "docs/zh/release_notes/release_notes.md",
  "docs/zh/security_statement/security_statement.md",
  "docs/zh/framework_feature_guide_pytorch/menu_framework_feature.md",
  "docs/zh/framework_feature_guide_pytorch/overview.md",
  "docs/zh/framework_feature_guide_pytorch/adaptation_description_extension.md",
  "docs/zh/framework_feature_guide_pytorch/adaptation_description_single.md",
  "docs/zh/framework_feature_guide_pytorch/custom_memory_allocator.md",
  "docs/zh/framework_feature_guide_pytorch/assisted_error_locating.md",
  "docs/zh/troubleshooting/menu_troubleshooting.md",
];

function rawUrl(branch, filePath) {
  const normalized = filePath.replace(/^\//, "").replace(/\\/g, "/");
  return `${GITCODE_BASE}/-/raw/${branch}/${normalized}`;
}

async function fetchUrl(url) {
  const res = await fetch(url, {
    headers: { "User-Agent": "torch-npu-docs-mcp/1.0" },
    signal: AbortSignal.timeout(15000),
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}: ${url}`);
  return res.text();
}

function ensureDir(dir) {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
}

const server = new Server(
  {
    name: "torch-npu-docs-fetcher",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "fetch_torch_npu_doc",
      description:
        "从 GitCode (https://gitcode.com/Ascend/pytorch) 抓取指定分支、指定路径的单个文档内容。可选择性保存到 skill 目录下的 fetched_docs 文件夹。分支示例: v2.7.1-7.3.0, v2.6.0-7.3.0, master",
      inputSchema: {
        type: "object",
        properties: {
          branch: {
            type: "string",
            description: "Git 分支或 tag，如 v2.7.1-7.3.0，不传则默认 v2.7.1-7.3.0",
            default: DEFAULT_BRANCH,
          },
          path: {
            type: "string",
            description:
              "仓库内文件路径，如 README.zh.md 或 docs/zh/overview/product_overview.md",
          },
          save_to_skill: {
            type: "boolean",
            description: "是否保存到 .cursor/skills/torch-npu/fetched_docs/<branch>/",
            default: true,
          },
        },
        required: ["path"],
      },
    },
    {
      name: "fetch_torch_npu_docs_batch",
      description:
        "批量抓取 torch_npu 常用中文文档到 skill 目录。可指定分支，不指定路径则使用内置的常用文档列表（与 reference.md 对应）。",
      inputSchema: {
        type: "object",
        properties: {
          branch: {
            type: "string",
            description: "Git 分支，如 v2.7.1-7.3.0",
            default: DEFAULT_BRANCH,
          },
          paths: {
            type: "array",
            items: { type: "string" },
            description:
              "要抓取的文件路径列表。不传则使用内置 DOC_PATHS_ZH 列表",
          },
        },
      },
    },
    {
      name: "list_torch_npu_doc_paths",
      description:
        "列出 MCP 内置的常用 torch_npu 中文文档路径列表，便于用户或 fetch_torch_npu_docs_batch 使用。",
      inputSchema: { type: "object", properties: {} },
    },
  ],
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  const skillRoot = path.resolve(__dirname, "..");
  const fetchedDir = path.join(skillRoot, "fetched_docs");

  try {
    if (name === "list_torch_npu_doc_paths") {
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(
              { paths: DOC_PATHS_ZH, hint: "可用于 fetch_torch_npu_docs_batch 的 paths 参数" },
              null,
              2
            ),
          },
        ],
      };
    }

    if (name === "fetch_torch_npu_doc") {
      const branch = (args && args.branch) || DEFAULT_BRANCH;
      const filePath = args && args.path;
      const saveToSkill = args && args.save_to_skill !== false;
      if (!filePath) {
        return {
          content: [{ type: "text", text: "错误: 缺少必填参数 path" }],
          isError: true,
        };
      }
      const url = rawUrl(branch, filePath);
      const text = await fetchUrl(url);
      if (saveToSkill) {
        const outDir = path.join(fetchedDir, branch, path.dirname(filePath));
        const outFile = path.join(fetchedDir, branch, filePath);
        ensureDir(outDir);
        fs.writeFileSync(outFile, text, "utf8");
      }
      return {
        content: [
          {
            type: "text",
            text: saveToSkill
              ? `已抓取并保存: ${filePath}\n保存位置: ${path.join(fetchedDir, branch, filePath)}\n\n--- 内容预览（前 2000 字）---\n${text.slice(0, 2000)}${text.length > 2000 ? "\n..." : ""}`
              : text.slice(0, 8000) + (text.length > 8000 ? "\n..." : ""),
          },
        ],
      };
    }

    if (name === "fetch_torch_npu_docs_batch") {
      const branch = (args && args.branch) || DEFAULT_BRANCH;
      const paths = (args && args.paths && args.paths.length) ? args.paths : DOC_PATHS_ZH;
      const results = [];
      const outBase = path.join(fetchedDir, branch);
      ensureDir(outBase);
      for (const filePath of paths) {
        try {
          const url = rawUrl(branch, filePath);
          const text = await fetchUrl(url);
          const outFile = path.join(outBase, filePath);
          ensureDir(path.dirname(outFile));
          fs.writeFileSync(outFile, text, "utf8");
          results.push({ path: filePath, ok: true });
        } catch (e) {
          results.push({ path: filePath, ok: false, error: e.message });
        }
      }
      return {
        content: [
          {
            type: "text",
            text: `批量抓取完成 (branch=${branch})\n保存目录: ${outBase}\n\n${JSON.stringify(results, null, 2)}`,
          },
        ],
      };
    }

    return {
      content: [{ type: "text", text: `未知工具: ${name}` }],
      isError: true,
    };
  } catch (err) {
    return {
      content: [{ type: "text", text: `执行失败: ${err.message}` }],
      isError: true,
    };
  }
});

const transport = new StdioServerTransport();
await server.connect(transport);
process.stderr.write("torch-npu-docs-fetcher MCP server running on stdio\n");
