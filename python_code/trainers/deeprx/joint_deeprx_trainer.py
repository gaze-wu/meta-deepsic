from python_code.detectors.deep_rx_detector import DeepRXDetector
from python_code.trainers.deeprx.rx_trainer import RXTrainer
from python_code.utils.config_singleton import Config
import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
conf = Config()


class JointDeepRXTrainer(RXTrainer):
    """
    Trainer for the DeepRX model.
    """

    def __init__(self):
        super().__init__()
        self.self_supervised = False

    def __str__(self):
        return 'DeepRX'

    def initialize_detector(self):
        """
        Loads the DeepRX detector
        """
        self.detector = DeepRXDetector(self.total_frame_size)

    def train_model(self, net, x_train, y_train, max_epochs):
        """
        Trains the DeepRX Network

        Parameters
        ----------
        net: an instance of the DeepSICNet class to be trained.
        k_m_fYtrain:  dictionary
                      The training data dictionary to be used for optimizing the underlying DeepSICNet network.
        -------

        """
        opt = torch.optim.Adam(net.parameters(), lr=conf.lr)
        crt = torch.nn.BCELoss().to(device)
        m = torch.nn.Sigmoid()
        net.set_state('train')
        net = net.to(device)
        for _ in range(max_epochs):
            opt.zero_grad()
            out = net(y_train)
            loss = crt(input=m(out), target=x_train)
            loss.backward()
            opt.step()

    def online_train_loop(self, x_train, y_train, model, max_epochs):
        pass

    def predict(self, y_test):
        self.detector.set_state('test')
        return self.detector(y_test)

    def train_loop(self, x_train, y_train, max_epochs, phase):
        self.train_model(self.detector, x_train, y_train, max_epochs)


if __name__ == "__main__":
    deep_rx_trainer = JointDeepRXTrainer()
    deep_rx_trainer.train()
