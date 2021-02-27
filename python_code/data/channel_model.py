import torch


class ChannelModel:
    @staticmethod
    def calculate_channel(N, K) -> torch.Tensor:
        pass

    @staticmethod
    def get_channel(channel_mode, N, K):
        if channel_mode == 'SED':
            H = SEDChannel.calculate_channel(N, K)
        elif channel_mode == 'Gaussian':
            H = GaussianChannel.calculate_channel(N, K)
        else:
            raise NotImplementedError
        return H


class SEDChannel(ChannelModel):
    @staticmethod
    def calculate_channel(N, K) -> torch.Tensor:
        H_row = torch.FloatTensor([i for i in range(N)])
        H_row = H_row.repeat([K, 1]).t()
        H_column = torch.FloatTensor([i for i in range(K)])
        H_column = H_column.repeat([N, 1])
        H = torch.exp(-torch.abs(H_row - H_column))
        return H


class GaussianChannel(ChannelModel):
    @staticmethod
    def calculate_channel(N, K) -> torch.Tensor:
        return torch.randn(N, K)
