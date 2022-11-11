from window import GLUTWindow
import EulerOperator
import numpy as np


if __name__ == "__main__":
    # 建立初始点，并初始化solid
    s, v = EulerOperator.mvfs(np.array([-1.0, -1.0, 0.0]))
    l = s.sfaces[0].flout

    # 绘制外圈
    EulerOperator.mev(l, s.sverts[-1], np.array([1.0, -1.0, 0.0]))
    EulerOperator.mev(l, s.sverts[-1], np.array([1.0, 1.0, 0.0]))
    EulerOperator.mev(l, s.sverts[-1], np.array([-1.0, 1.0, 0.0]))
    EulerOperator.mef(l, s.sverts[-1], s.sverts[0])

    # 绘制第一个内圈
    EulerOperator.mev(l, s.sverts[3], np.array([-0.75, 0.75, 0.0]))
    EulerOperator.mev(l, s.sverts[-1], np.array([-0.75, 0.25, 0.0]))
    EulerOperator.mev(l, s.sverts[-1], np.array([-0.25, 0.25, 0.0]))
    EulerOperator.mev(l, s.sverts[-1], np.array([-0.25, 0.75, 0.0]))
    EulerOperator.mef(l, s.sverts[4], s.sverts[-1])
    EulerOperator.kemr(l, s.sverts[3], s.sverts[4])
    # EulerOperator.kfmrh(l.lface, s.sfaces[-1])

    # 绘制第二个内圈
    EulerOperator.mev(l, s.sverts[3], np.array([0.0, 0.0, 0.0]))
    EulerOperator.mev(l, s.sverts[-1], np.array([0.0, -0.5, 0.0]))
    EulerOperator.mev(l, s.sverts[-1], np.array([0.5, -0.5, 0.0]))
    EulerOperator.mev(l, s.sverts[-1], np.array([0.5, 0.0, 0.0]))
    EulerOperator.mef(l, s.sverts[8], s.sverts[-1])
    EulerOperator.kemr(l, s.sverts[3], s.sverts[8])
    # EulerOperator.kfmrh(l.lface, s.sfaces[-1])

    EulerOperator.sweep(s, np.array([0.0, 0.0, 1.0]))
    window = GLUTWindow(s)
    window.run()
