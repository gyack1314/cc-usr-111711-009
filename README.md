# 跨行业供应韧性方案分析

现有程序从有来源的供应、需求、证书和业务上下文记录形成单期分配，并按已知时间保存可复算结果。备用库存、合同优先级与恢复次序需共享。

当前输入由合作方的本地合成材料组成，不连接实时行业系统。报告中的原文摘要用于追溯，不能由这份示例推断真实行业产能或减排量。

在项目根目录执行：

    python -m unittest discover -s tests -v
    python -m compileall -q fuel_lab tests
    python -m fuel_lab.cli inspect data/example.json

Dockerfile 提供 Linux 运行环境；docker build -t supply-resilience . 构建，docker run --rm supply-resilience 运行样例。

现有备用库存与检修规则位于 context.py，参与资格检查和报告解释；数据修订保留原始版本。
