# 递归网络中的长短期记忆

## 递归网络 RNN

Recurrent Neural Network 的神经单元工作在离散时间序列中。
在某个时刻，神经元将与其连接的输入神经元在上一个时刻的输出进行加权求和，经过一个激活函数，产生这一时刻的输出。

$y^i(t) = f\left(\sum_j w_{ij} y^j(t-1)\right)$



