#!/usr/bin/env python

from __future__ import division, print_function, absolute_import

import numpy as np
from numpy.testing import run_module_suite, assert_allclose, assert_

import pywt


def test_idwtn_reconstruct():
    data = np.array([
        [[0, 4, 1, 5, 1, 4],
         [0 ,5, 6, 3, 2, 1],
         [2, 5,19, 4,19, 1]],
        [[1, 5, 1, 2, 3, 4],
         [7,12, 6,52, 7, 8],
         [5, 2, 6,78,12, 2]]])
    wavelet = pywt.Wavelet('haar')

    d = pywt.dwtn(data, wavelet)

    # idwtn creates even-length shapes (2x dwtn size)
    original_shape = [slice(None, s) for s in data.shape]
    assert_allclose(data, pywt.idwtn(d, wavelet)[original_shape],
                    rtol=1e-13, atol=1e-13)


def test_idwtn_idwt2():
    data = np.array([
        [0, 4, 1, 5, 1, 4],
        [0 ,5, 6, 3, 2, 1],
        [2, 5,19, 4,19, 1]])

    wavelet = pywt.Wavelet('haar')

    LL, (HL, LH, HH) = pywt.dwt2(data, wavelet)
    d = {'aa': LL, 'da': HL, 'ad': LH, 'dd': HH}

    assert_allclose(pywt.idwt2((LL, (HL, LH, HH)), wavelet),
                    pywt.idwtn(d, wavelet), rtol=1e-14, atol=1e-14)


def test_idwtn_missing():
    # Test to confirm missing data behave as zeroes
    data = np.array([
        [0, 4, 1, 5, 1, 4],
        [0 ,5, 6, 3, 2, 1],
        [2, 5,19, 4,19, 1]])

    wavelet = pywt.Wavelet('haar')

    LL, (HL, _, HH) = pywt.dwt2(data, wavelet)
    d = {'aa': LL, 'da': HL, 'dd': HH}

    assert_allclose(pywt.idwt2((LL, (HL, None, HH)), wavelet),
                    pywt.idwtn(d, 'haar'), atol=1e-15)


def test_idwtn_take():
    data = np.array([
        [[1, 4, 1, 5, 1, 4],
         [0 ,5, 6, 3, 2, 1],
         [2, 5,19, 4,19, 1]],
        [[1, 5, 1, 2, 3, 4],
         [7,12, 6,52, 7, 8],
         [5, 2, 6,78,12, 2]]])
    wavelet = pywt.Wavelet('haar')

    d = pywt.dwtn(data, wavelet)

    assert_(data.shape != pywt.idwtn(d, wavelet).shape)
    assert_allclose(data, pywt.idwtn(d, wavelet, data.shape), atol=1e-15)


if __name__ == '__main__':
    run_module_suite()
