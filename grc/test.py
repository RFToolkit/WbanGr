#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# Author: root
# GNU Radio version: 3.9.8.0

from distutils.version import StrictVersion

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
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import eng_notation
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
import math
from gnuradio import blocks
from gnuradio import digital
from gnuradio import filter
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import soapy
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
import foo
import ieee802_15_4



from gnuradio import qtgui

class test(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
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

        self.settings = Qt.QSettings("GNU Radio", "test")

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
        self.channel = channel = 49
        self.freq = freq = 2400500000 + 1000000*(channel - 11)
        self.symb0 = symb0 = 4
        self.symb = symb = 16
        self.samp_rate = samp_rate = 1000000
        self.rx_gain = rx_gain = 5
        self.page_label = page_label = 0
        self.if_gain = if_gain = 30
        self.freqd = freqd = 926
        self.freq_label = freq_label = freq / 1000000000.0
        self.bt = bt = 15
        self.bb_gain = bb_gain = 30

        ##################################################
        # Blocks
        ##################################################
        self._symb0_range = Range(2, 50, 1, 4, 200)
        self._symb0_win = RangeWidget(self._symb0_range, self.set_symb0, "symb0", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._symb0_win, 80, 0, 1, 1)
        for r in range(80, 81):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._symb_range = Range(2, 50, 1, 16, 200)
        self._symb_win = RangeWidget(self._symb_range, self.set_symb, "symb", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._symb_win, 90, 0, 1, 1)
        for r in range(90, 91):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._bt_range = Range(0, 50, 1, 15, 200)
        self._bt_win = RangeWidget(self._bt_range, self.set_bt, "bt", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._bt_win, 60, 0, 1, 1)
        for r in range(60, 61):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.soapy_hackrf_source_0 = None
        dev = 'driver=hackrf'
        stream_args = ''
        tune_args = ['']
        settings = ['']

        self.soapy_hackrf_source_0 = soapy.source(dev, "fc32", 1, '',
                                  stream_args, tune_args, settings)
        self.soapy_hackrf_source_0.set_sample_rate(0, samp_rate)
        self.soapy_hackrf_source_0.set_bandwidth(0, 0)
        self.soapy_hackrf_source_0.set_frequency(0, freq)
        self.soapy_hackrf_source_0.set_gain(0, 'AMP', False)
        self.soapy_hackrf_source_0.set_gain(0, 'LNA', min(max(16, 0.0), 40.0))
        self.soapy_hackrf_source_0.set_gain(0, 'VGA', min(max(16, 0.0), 62.0))
        self.single_pole_iir_filter_xx_0 = filter.single_pole_iir_filter_ff(0.000150, 1)
        self._rx_gain_range = Range(0, 50, 1, 5, 200)
        self._rx_gain_win = RangeWidget(self._rx_gain_range, self.set_rx_gain, "'rx_gain'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._rx_gain_win, 96, 0, 1, 1)
        for r in range(96, 97):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_sink_x_0 = qtgui.sink_c(
            1024, #fftsize
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True, #plotconst
            None # parent
        )
        self.qtgui_sink_x_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.qwidget(), Qt.QWidget)

        self.qtgui_sink_x_0.enable_rf_freq(False)

        self.top_layout.addWidget(self._qtgui_sink_x_0_win)
        self.qtgui_const_sink_x_1_1 = qtgui.const_sink_c(
            1024, #size
            "Rx", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_const_sink_x_1_1.set_update_time(0.1)
        self.qtgui_const_sink_x_1_1.set_y_axis(-0.4, 0.4)
        self.qtgui_const_sink_x_1_1.set_x_axis(-0.4, 0.4)
        self.qtgui_const_sink_x_1_1.set_trigger_mode(qtgui.TRIG_MODE_AUTO, qtgui.TRIG_SLOPE_POS, 0.4, 0, "")
        self.qtgui_const_sink_x_1_1.enable_autoscale(False)
        self.qtgui_const_sink_x_1_1.enable_grid(False)
        self.qtgui_const_sink_x_1_1.enable_axis_labels(True)


        labels = ['Rx raw', 'DQPSK Soft', 'MPSK', 'Unbuf', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["Dark Blue", "red", "yellow", "cyan", "red",
            "red", "red", "red", "red", "red"]
        styles = [1, 0, 4, 5, 0,
            0, 0, 0, 0, 0]
        markers = [9, 7, 6, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_1_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_1_1.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_1_1.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_1_1.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_1_1.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_1_1.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_1_1.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_1_1_win = sip.wrapinstance(self.qtgui_const_sink_x_1_1.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_const_sink_x_1_1_win, 1, 0, 1, 4)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._page_label_tool_bar = Qt.QToolBar(self)

        if None:
            self._page_label_formatter = None
        else:
            self._page_label_formatter = lambda x: str(x)

        self._page_label_tool_bar.addWidget(Qt.QLabel("Channel Page"))
        self._page_label_label = Qt.QLabel(str(self._page_label_formatter(self.page_label)))
        self._page_label_tool_bar.addWidget(self._page_label_label)
        self.top_grid_layout.addWidget(self._page_label_tool_bar, 0, 0, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            1,
            firdes.low_pass(
                1,
                samp_rate,
                samp_rate/2,
                samp_rate/4,
                window.WIN_HAMMING,
                6.76))
        self._if_gain_range = Range(0, 50, 1, 30, 200)
        self._if_gain_win = RangeWidget(self._if_gain_range, self.set_if_gain, "if_gain", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._if_gain_win, 97, 0, 1, 1)
        for r in range(97, 98):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.ieee802_15_4_packet_sink_0 = ieee802_15_4.packet_sink(bt)
        self._freqd_range = Range(926, 6000, 1, 926, 200)
        self._freqd_win = RangeWidget(self._freqd_range, self.set_freqd, "freqd", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._freqd_win, 40, 0, 1, 2)
        for r in range(40, 41):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._freq_label_tool_bar = Qt.QToolBar(self)

        if None:
            self._freq_label_formatter = None
        else:
            self._freq_label_formatter = lambda x: eng_notation.num_to_str(x)

        self._freq_label_tool_bar.addWidget(Qt.QLabel("Frequency (GHz)"))
        self._freq_label_label = Qt.QLabel(str(self._freq_label_formatter(self.freq_label)))
        self._freq_label_tool_bar.addWidget(self._freq_label_label)
        self.top_grid_layout.addWidget(self._freq_label_tool_bar, 2, 0, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.foo_wireshark_connector_0 = foo.wireshark_connector(195, False)
        self.digital_symbol_sync_xx_0 = digital.symbol_sync_ff(
            digital.TED_MENGALI_AND_DANDREA_GMSK,
            symb,
            0.045,
            1.0,
            1.0,
            1.5,
            symb0,
            digital.constellation_bpsk().base(),
            digital.IR_MMSE_8TAP,
            128,
            [])
        self.digital_clock_recovery_mm_xx_0 = digital.clock_recovery_mm_ff(2, 0.00225, 0.5, 0.03, 0.0002)
        # Create the options list
        self._channel_options = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49]
        # Create the labels list
        self._channel_labels = map(str, self._channel_options)
        # Create the combo box
        self._channel_tool_bar = Qt.QToolBar(self)
        self._channel_tool_bar.addWidget(Qt.QLabel("Channel Number" + ": "))
        self._channel_combo_box = Qt.QComboBox()
        self._channel_tool_bar.addWidget(self._channel_combo_box)
        for _label in self._channel_labels: self._channel_combo_box.addItem(_label)
        self._channel_callback = lambda i: Qt.QMetaObject.invokeMethod(self._channel_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._channel_options.index(i)))
        self._channel_callback(self.channel)
        self._channel_combo_box.currentIndexChanged.connect(
            lambda i: self.set_channel(self._channel_options[i]))
        # Create the radio buttons
        self.top_grid_layout.addWidget(self._channel_tool_bar, 99, 0, 1, 1)
        for r in range(99, 100):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate*4,True)
        self.blocks_sub_xx_0 = blocks.sub_ff(1)
        self.blocks_file_sink_0_0_1_0 = blocks.file_sink(gr.sizeof_char*1, '/opt/gr-wban/wpan.pcap', False)
        self.blocks_file_sink_0_0_1_0.set_unbuffered(True)
        self._bb_gain_range = Range(0, 50, 1, 30, 200)
        self._bb_gain_win = RangeWidget(self._bb_gain_range, self.set_bb_gain, "BB", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._bb_gain_win, 98, 0, 1, 1)
        for r in range(98, 99):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.analog_simple_squelch_cc_0 = analog.simple_squelch_cc(-15, 1)
        self.analog_quadrature_demod_cf_0 = analog.quadrature_demod_cf(1)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.ieee802_15_4_packet_sink_0, 'out'), (self.foo_wireshark_connector_0, 'in'))
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.blocks_sub_xx_0, 0))
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.single_pole_iir_filter_xx_0, 0))
        self.connect((self.analog_simple_squelch_cc_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_sub_xx_0, 0), (self.digital_clock_recovery_mm_xx_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.digital_clock_recovery_mm_xx_0, 0), (self.digital_symbol_sync_xx_0, 0))
        self.connect((self.digital_symbol_sync_xx_0, 0), (self.ieee802_15_4_packet_sink_0, 0))
        self.connect((self.foo_wireshark_connector_0, 0), (self.blocks_file_sink_0_0_1_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.analog_quadrature_demod_cf_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.qtgui_const_sink_x_1_1, 0))
        self.connect((self.low_pass_filter_0, 0), (self.qtgui_sink_x_0, 0))
        self.connect((self.single_pole_iir_filter_xx_0, 0), (self.blocks_sub_xx_0, 1))
        self.connect((self.soapy_hackrf_source_0, 0), (self.analog_simple_squelch_cc_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "test")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_channel(self):
        return self.channel

    def set_channel(self, channel):
        self.channel = channel
        self._channel_callback(self.channel)
        self.set_freq(2400500000 + 1000000*(self.channel - 11))

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.set_freq_label(self.freq / 1000000000.0)
        self.soapy_hackrf_source_0.set_frequency(0, self.freq)

    def get_symb0(self):
        return self.symb0

    def set_symb0(self, symb0):
        self.symb0 = symb0

    def get_symb(self):
        return self.symb

    def set_symb(self, symb):
        self.symb = symb

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0.set_sample_rate(self.samp_rate*4)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.samp_rate/2, self.samp_rate/4, window.WIN_HAMMING, 6.76))
        self.qtgui_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.soapy_hackrf_source_0.set_sample_rate(0, self.samp_rate)

    def get_rx_gain(self):
        return self.rx_gain

    def set_rx_gain(self, rx_gain):
        self.rx_gain = rx_gain

    def get_page_label(self):
        return self.page_label

    def set_page_label(self, page_label):
        self.page_label = page_label
        Qt.QMetaObject.invokeMethod(self._page_label_label, "setText", Qt.Q_ARG("QString", str(self._page_label_formatter(self.page_label))))

    def get_if_gain(self):
        return self.if_gain

    def set_if_gain(self, if_gain):
        self.if_gain = if_gain

    def get_freqd(self):
        return self.freqd

    def set_freqd(self, freqd):
        self.freqd = freqd

    def get_freq_label(self):
        return self.freq_label

    def set_freq_label(self, freq_label):
        self.freq_label = freq_label
        Qt.QMetaObject.invokeMethod(self._freq_label_label, "setText", Qt.Q_ARG("QString", str(self._freq_label_formatter(self.freq_label))))

    def get_bt(self):
        return self.bt

    def set_bt(self, bt):
        self.bt = bt

    def get_bb_gain(self):
        return self.bb_gain

    def set_bb_gain(self, bb_gain):
        self.bb_gain = bb_gain




def main(top_block_cls=test, options=None):

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
