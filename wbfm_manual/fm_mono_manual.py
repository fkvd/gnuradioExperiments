#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: FM Mono Manual
# Author: fkvd
# GNU Radio version: 3.10.3.0

from packaging.version import Version as StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import filter
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
import osmosdr
import time



from gnuradio import qtgui

class fm_mono_manual(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "FM Mono Manual", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("FM Mono Manual")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "fm_mono_manual")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.volumeControl = volumeControl = 0.4
        self.samp_rate = samp_rate = 2400000

        ##################################################
        # Blocks
        ##################################################
        self._volumeControl_range = Range(0, 1, 0.1, 0.4, 200)
        self._volumeControl_win = RangeWidget(self._volumeControl_range, self.set_volumeControl, "'volumeControl'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._volumeControl_win)
        self.rtlsdr_source_0_0 = osmosdr.source(
            args="numchan=" + str(1) + " " + ""
        )
        self.rtlsdr_source_0_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.rtlsdr_source_0_0.set_sample_rate(samp_rate)
        self.rtlsdr_source_0_0.set_center_freq(103.4e6, 0)
        self.rtlsdr_source_0_0.set_freq_corr(0, 0)
        self.rtlsdr_source_0_0.set_dc_offset_mode(0, 0)
        self.rtlsdr_source_0_0.set_iq_balance_mode(0, 0)
        self.rtlsdr_source_0_0.set_gain_mode(False, 0)
        self.rtlsdr_source_0_0.set_gain(20, 0)
        self.rtlsdr_source_0_0.set_if_gain(20, 0)
        self.rtlsdr_source_0_0.set_bb_gain(20, 0)
        self.rtlsdr_source_0_0.set_antenna('', 0)
        self.rtlsdr_source_0_0.set_bandwidth(0, 0)
        self.qtgui_freq_sink_x_1 = qtgui.freq_sink_f(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            (samp_rate/10), #bw
            "Deemphasis", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_1.set_update_time(0.10)
        self.qtgui_freq_sink_x_1.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_1.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_1.enable_autoscale(False)
        self.qtgui_freq_sink_x_1.enable_grid(False)
        self.qtgui_freq_sink_x_1.set_fft_average(1.0)
        self.qtgui_freq_sink_x_1.enable_axis_labels(True)
        self.qtgui_freq_sink_x_1.enable_control_panel(False)
        self.qtgui_freq_sink_x_1.set_fft_window_normalized(False)


        self.qtgui_freq_sink_x_1.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_1.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_1_win = sip.wrapinstance(self.qtgui_freq_sink_x_1.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_1_win)
        self.low_pass_filter_0 = filter.fir_filter_fff(
            5,
            firdes.low_pass(
                1,
                (samp_rate/10),
                15000,
                1000,
                window.WIN_HAMMING,
                6.76))
        self.freq_xlating_fir_filter_xxx_0_0 = filter.freq_xlating_fir_filter_ccc(10, firdes.low_pass(1, samp_rate, 100000,10000), 100000, samp_rate)
        self.blocks_wavfile_sink_0_0 = blocks.wavfile_sink(
            'decodedMonoFM.wav',
            1,
            48000,
            blocks.FORMAT_WAV,
            blocks.FORMAT_PCM_16,
            False
            )
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(volumeControl)
        self.blocks_multiply_conjugate_cc_0 = blocks.multiply_conjugate_cc(1)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_gr_complex*1, 1)
        self.blocks_complex_to_magphase_0 = blocks.complex_to_magphase(1)
        self.audio_sink_0_0 = audio.sink(48000, '', True)
        self.analog_fm_deemph_0 = analog.fm_deemph(fs=(samp_rate/10), tau=(75e-6))


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_fm_deemph_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.analog_fm_deemph_0, 0), (self.qtgui_freq_sink_x_1, 0))
        self.connect((self.blocks_complex_to_magphase_0, 1), (self.analog_fm_deemph_0, 0))
        self.connect((self.blocks_complex_to_magphase_0, 0), (self.blocks_null_sink_0, 0))
        self.connect((self.blocks_delay_0, 0), (self.blocks_multiply_conjugate_cc_0, 1))
        self.connect((self.blocks_multiply_conjugate_cc_0, 0), (self.blocks_complex_to_magphase_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.audio_sink_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_wavfile_sink_0_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0_0, 0), (self.blocks_delay_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0_0, 0), (self.blocks_multiply_conjugate_cc_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.rtlsdr_source_0_0, 0), (self.freq_xlating_fir_filter_xxx_0_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "fm_mono_manual")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_volumeControl(self):
        return self.volumeControl

    def set_volumeControl(self, volumeControl):
        self.volumeControl = volumeControl
        self.blocks_multiply_const_vxx_0.set_k(self.volumeControl)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.freq_xlating_fir_filter_xxx_0_0.set_taps(firdes.low_pass(1, self.samp_rate, 100000,10000))
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, (self.samp_rate/10), 15000, 1000, window.WIN_HAMMING, 6.76))
        self.qtgui_freq_sink_x_1.set_frequency_range(0, (self.samp_rate/10))
        self.rtlsdr_source_0_0.set_sample_rate(self.samp_rate)




def main(top_block_cls=fm_mono_manual, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
