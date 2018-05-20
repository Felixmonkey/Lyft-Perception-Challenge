import torch
import torch.nn as nn
import torch.nn.functional as F

eps = 1e-8

def dice_loss(preds, trues):
    batch = preds.size(0)
    classes = preds.size(1)
    preds = preds.view(batch, classes, -1)
    trues = trues.view(batch, classes, -1)
    weights = torch.clamp(trues.sum(-1), 0., 1.)
    intersection = (preds * trues).sum(2)
    scores = 2. * (intersection + eps) / (preds.sum(2) + trues.sum(2) + eps)
    scores = scores * weights
    score = scores.sum() / weights.sum()
    return torch.clamp(score, 0., 1.)


class DiceLoss(nn.Module):
    def __init__(self):
        super().__init__()

    def forward(self, input, target):
        return 1 - dice_loss(input, target)


class BCEDiceLoss(nn.Module):
    def __init__(self, bce_coef):
        super().__init__()
        self.dice = DiceLoss()
        self.bce_coef = bce_coef

    def forward(self, input, target):
        bce = nn.BCELoss()(input, target)
        dice = self.dice(input, target)
        return self.bce_coef * bce + dice
