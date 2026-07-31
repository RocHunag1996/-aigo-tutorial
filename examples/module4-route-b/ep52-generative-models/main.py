"""
AIGO 教程系列 - 路线 B·模拟方法创新
ep52-generative-models: 生成式模型

演示用简单 VAE 思路生成材料特征向量（用 numpy 随机模拟）。
说明当前局限和未来方向。
"""
import numpy as np


# ── 模拟 VAE 的核心组件 ─────────────────────────────────────
class SimpleVAE:
    """
    极简 VAE 模拟（纯 numpy，仅用于教学演示）。
    真实 VAE 需要 PyTorch/TensorFlow，这里用随机采样模拟。
    """

    def __init__(self, latent_dim=4, feature_dim=10):
        self.latent_dim = latent_dim
        self.feature_dim = feature_dim
        # 模拟编码器参数
        self.W_enc = np.random.randn(feature_dim, latent_dim * 2) * 0.1
        self.b_enc = np.zeros(latent_dim * 2)
        # 模拟解码器参数
        self.W_dec = np.random.randn(latent_dim, feature_dim) * 0.1
        self.b_dec = np.zeros(feature_dim)

    def encode(self, x):
        """编码器: x -> (mu, log_var)"""
        h = x @ self.W_enc + self.b_enc
        mu = h[:, :self.latent_dim]
        log_var = h[:, self.latent_dim:]
        return mu, log_var

    def reparameterize(self, mu, log_var):
        """重参数化技巧: z = mu + sigma * epsilon"""
        std = np.exp(0.5 * log_var)
        epsilon = np.random.randn(*mu.shape)
        return mu + std * epsilon

    def decode(self, z):
        """解码器: z -> x_reconstructed"""
        return z @ self.W_dec + self.b_dec

    def forward(self, x):
        """前向传播: x -> x_reconstructed, mu, log_var"""
        mu, log_var = self.encode(x)
        z = self.reparameterize(mu, log_var)
        x_recon = self.decode(z)
        return x_recon, mu, log_var


def vae_loss(x, x_recon, mu, log_var):
    """
    VAE 损失 = 重构损失 + KL 散度。
    重构损失: MSE
    KL 散度: -0.5 * sum(1 + log_var - mu^2 - exp(log_var))
    """
    recon_loss = np.mean((x - x_recon) ** 2)
    kl_loss = -0.5 * np.mean(1 + log_var - mu**2 - np.exp(log_var))
    return recon_loss + kl_loss, recon_loss, kl_loss


def generate_material_features(vae, n_samples=10, temperature=1.0):
    """
    从潜空间采样生成新材料特征向量。
    temperature 控制生成多样性。
    """
    z = np.random.randn(n_samples, vae.latent_dim) * temperature
    features = vae.decode(z)
    return features


def demo_training_loop(n_epochs=30):
    """演示 VAE 训练循环（模拟）。"""
    np.random.seed(42)

    feature_dim = 10
    latent_dim = 4
    n_samples = 50

    vae = SimpleVAE(latent_dim=latent_dim, feature_dim=feature_dim)

    # 模拟训练数据（材料特征向量）
    X_train = np.random.randn(n_samples, feature_dim) * 0.5 + 1.0

    print(f"\n  VAE 训练参数：")
    print(f"  特征维度: {feature_dim}, 潜空间维度: {latent_dim}")
    print(f"  训练样本: {n_samples}")
    print(f"\n  {'轮次':>4s} | {'总损失':>8s} | {'重构损失':>8s} | {'KL散度':>8s}")
    print("  " + "-" * 42)

    for epoch in range(n_epochs):
        # 模拟训练（实际应更新权重）
        x_recon, mu, log_var = vae.forward(X_train)

        # 模拟权重更新效果：逐步降低损失
        decay = np.exp(-epoch / 10)
        noise_scale = 0.5 * decay
        x_recon = X_train + np.random.randn(*X_train.shape) * noise_scale
        log_var = np.log(0.1 + 0.5 * decay) * np.ones_like(mu)

        total_loss, recon_loss, kl_loss = vae_loss(X_train, x_recon, mu, log_var)

        if (epoch + 1) % 5 == 0 or epoch == 0:
            print(f"  {epoch+1:>4d} | {total_loss:>8.4f} | {recon_loss:>8.4f} | {kl_loss:>8.4f}")

    return vae


def main():
    print("=" * 60)
    print("  ep52 - 生成式模型：VAE 生成材料特征")
    print("=" * 60)

    print("\n  VAE (Variational Autoencoder) 核心思想：")
    print("  编码器: 材料特征 x -> 潜变量 z 的分布 q(z|x)")
    print("  解码器: 潜变量 z -> 重构特征 x'")
    print("  训练: 最小化重构误差 + KL 散度正则化")
    print("  生成: 从先验 p(z)=N(0,I) 采样 z -> 解码得到新材料特征")

    # 训练演示
    print("\n  Step 1: 训练 VAE（模拟）")
    vae = demo_training_loop(n_epochs=30)

    # 生成新材料
    print("\n  Step 2: 从潜空间生成新材料特征")
    generated = generate_material_features(vae, n_samples=5, temperature=1.0)

    feature_names = [f"feat_{i+1}" for i in range(generated.shape[1])]
    print(f"\n  生成的 {generated.shape[0]} 个材料特征向量：")
    print(f"  {'样本':<6s}", end="")
    for name in feature_names[:5]:
        print(f" {name:<10s}", end="")
    print(" ...")
    print("  " + "-" * 56)
    for i, feat in enumerate(generated):
        print(f"  {i+1:<6d}", end="")
        for v in feat[:5]:
            print(f" {v:<10.3f}", end="")
        print(" ...")

    # 潜空间插值
    print("\n  Step 3: 潜空间插值（材料性质渐变）")
    z1 = np.array([1, 0, 0, 0], dtype=float)
    z2 = np.array([0, 1, 0, 0], dtype=float)
    print(f"  从 z1={z1} 到 z2={z2} 的插值：")
    for alpha in [0.0, 0.25, 0.5, 0.75, 1.0]:
        z_interp = (1 - alpha) * z1 + alpha * z2
        feat = vae.decode(z_interp.reshape(1, -1))[0]
        print(f"    alpha={alpha:.2f}: 特征前3维 = {feat[:3].round(3)}")

    print(f"\n  当前局限：")
    print("  - numpy 模拟的 VAE 没有真正学习，仅演示流程")
    print("  - 真实 VAE 需要 PyTorch + 大量 DFT 训练数据")
    print("  - 生成的特征需要反向映射到实际晶体结构")
    print("  - 当前生成模型还难以保证物理可行性（如稳定性）")
    print("  - 前沿方向: 扩散模型(Diffusion)、Flow Matching")


if __name__ == "__main__":
    main()
