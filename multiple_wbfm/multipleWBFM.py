#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Multiple WBFM Recorder
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

from gnuradio import analog
from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.filter import pfb
import osmosdr
import time



from gnuradio import qtgui

class multipleWBFM(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Multiple WBFM Recorder", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Multiple WBFM Recorder")
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

        self.settings = Qt.QSettings("GNU Radio", "multipleWBFM")

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
        self.samp_rate = samp_rate = 2.4e6
        self.pfb_taps = pfb_taps = firdes.low_pass_2(1, samp_rate, 125e3, 100e3, 60)
        self.frequency = frequency = 104.9e6

        ##################################################
        # Blocks
        ##################################################
        self.rtlsdr_source_0 = osmosdr.source(
            args="numchan=" + str(1) + " " + ""
        )
        self.rtlsdr_source_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.rtlsdr_source_0.set_sample_rate(samp_rate)
        self.rtlsdr_source_0.set_center_freq(frequency, 0)
        self.rtlsdr_source_0.set_freq_corr(0, 0)
        self.rtlsdr_source_0.set_dc_offset_mode(0, 0)
        self.rtlsdr_source_0.set_iq_balance_mode(0, 0)
        self.rtlsdr_source_0.set_gain_mode(False, 0)
        self.rtlsdr_source_0.set_gain(30, 0)
        self.rtlsdr_source_0.set_if_gain(20, 0)
        self.rtlsdr_source_0.set_bb_gain(20, 0)
        self.rtlsdr_source_0.set_antenna('', 0)
        self.rtlsdr_source_0.set_bandwidth(0, 0)
        self.rational_resampler_xxx_0_0_0 = filter.rational_resampler_fff(
                interpolation=48,
                decimation=50,
                taps=[],
                fractional_bw=0)
        self.rational_resampler_xxx_0_0 = filter.rational_resampler_fff(
                interpolation=48,
                decimation=50,
                taps=[],
                fractional_bw=0)
        self.pfb_channelizer_ccf_0 = pfb.channelizer_ccf(
            12,
            pfb_taps,
            1.0,
            100)
        self.pfb_channelizer_ccf_0.set_channel_map([0, 1, 2, 3 ,4 ,5 ,6,7,8,9,10,11])
        self.pfb_channelizer_ccf_0.declare_sample_delay(0)
        self.freq_xlating_fir_filter_xxx_0_0_0 = filter.freq_xlating_fir_filter_ccc(1, firdes.low_pass(1,samp_rate/12, 100000, 3000), 0, (samp_rate/12))
        self.freq_xlating_fir_filter_xxx_0_0 = filter.freq_xlating_fir_filter_ccc(1, firdes.low_pass(1,samp_rate/12, 100000, 3000), 0, (samp_rate/12))
        self.blocks_wavfile_sink_0_0 = blocks.wavfile_sink(
            '104.3.wav',
            1,
            48000,
            blocks.FORMAT_WAV,
            blocks.FORMAT_PCM_16,
            False
            )
        self.blocks_wavfile_sink_0 = blocks.wavfile_sink(
            '105.5.wav',
            1,
            48000,
            blocks.FORMAT_WAV,
            blocks.FORMAT_PCM_16,
            False
            )
        self.blocks_null_sink_0_2 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_0_1 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_0_0_2 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_0_0_1 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_0_0_0_2 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_0_0_0_1 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_0_0_0_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_0_0_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_0_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.analog_fm_demod_cf_0_0_0 = analog.fm_demod_cf(
        	channel_rate=(samp_rate/12),
        	audio_decim=4,
        	deviation=150000,
        	audio_pass=15000,
        	audio_stop=16000,
        	gain=1.0,
        	tau=(75e-6),
        )
        self.analog_fm_demod_cf_0_0 = analog.fm_demod_cf(
        	channel_rate=(samp_rate/12),
        	audio_decim=4,
        	deviation=150000,
        	audio_pass=15000,
        	audio_stop=16000,
        	gain=1.0,
        	tau=(75e-6),
        )


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_fm_demod_cf_0_0, 0), (self.rational_resampler_xxx_0_0, 0))
        self.connect((self.analog_fm_demod_cf_0_0_0, 0), (self.rational_resampler_xxx_0_0_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0_0, 0), (self.analog_fm_demod_cf_0_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0_0_0, 0), (self.analog_fm_demod_cf_0_0_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 0), (self.blocks_null_sink_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 1), (self.blocks_null_sink_0_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 2), (self.blocks_null_sink_0_0_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 4), (self.blocks_null_sink_0_0_0_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 7), (self.blocks_null_sink_0_0_0_1, 0))
        self.connect((self.pfb_channelizer_ccf_0, 11), (self.blocks_null_sink_0_0_0_2, 0))
        self.connect((self.pfb_channelizer_ccf_0, 6), (self.blocks_null_sink_0_0_1, 0))
        self.connect((self.pfb_channelizer_ccf_0, 10), (self.blocks_null_sink_0_0_2, 0))
        self.connect((self.pfb_channelizer_ccf_0, 5), (self.blocks_null_sink_0_1, 0))
        self.connect((self.pfb_channelizer_ccf_0, 8), (self.blocks_null_sink_0_2, 0))
        self.connect((self.pfb_channelizer_ccf_0, 3), (self.freq_xlating_fir_filter_xxx_0_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 9), (self.freq_xlating_fir_filter_xxx_0_0_0, 0))
        self.connect((self.rational_resampler_xxx_0_0, 0), (self.blocks_wavfile_sink_0, 0))
        self.connect((self.rational_resampler_xxx_0_0_0, 0), (self.blocks_wavfile_sink_0_0, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.pfb_channelizer_ccf_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "multipleWBFM")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_pfb_taps(firdes.low_pass_2(1, self.samp_rate, 125e3, 100e3, 60))
        self.freq_xlating_fir_filter_xxx_0_0.set_taps(firdes.low_pass(1,self.samp_rate/12, 100000, 3000))
        self.freq_xlating_fir_filter_xxx_0_0_0.set_taps(firdes.low_pass(1,self.samp_rate/12, 100000, 3000))
        self.rtlsdr_source_0.set_sample_rate(self.samp_rate)

    def get_pfb_taps(self):
        return self.pfb_taps

    def set_pfb_taps(self, pfb_taps):
        self.pfb_taps = pfb_taps
        self.pfb_channelizer_ccf_0.set_taps(self.pfb_taps)

    def get_frequency(self):
        return self.frequency

    def set_frequency(self, frequency):
        self.frequency = frequency
        self.rtlsdr_source_0.set_center_freq(self.frequency, 0)




def main(top_block_cls=multipleWBFM, options=None):

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
