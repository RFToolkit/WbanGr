#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: IEEE 802.15.4 Transceiver
# Author: Dimitrios-Georgios Akestoridis
# Description: A simplified version of Bastian Bloessl's GRC flow graph for an IEEE 802.15.4 transceiver.
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
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
import foo
import ieee802_15_4
import osmosdr
import time



from gnuradio import qtgui

class ieee802154_transceiver(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "IEEE 802.15.4 Transceiver", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("IEEE 802.15.4 Transceiver")
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

        self.settings = Qt.QSettings("GNU Radio", "ieee802154_transceiver")

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
        self.channel = channel = 20
        self.freq = freq = 2405000000 + 5000000*(channel - 11)
        self.symb0 = symb0 = 8
        self.symb = symb = 3
        self.samp_rate = samp_rate = 60000000
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
        self._symb0_range = Range(2, 50, 1, 8, 200)
        self._symb0_win = RangeWidget(self._symb0_range, self.set_symb0, "symb0", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._symb0_win, 80, 0, 1, 1)
        for r in range(80, 81):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._symb_range = Range(2, 50, 1, 3, 200)
        self._symb_win = RangeWidget(self._symb_range, self.set_symb, "symb", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._symb_win, 90, 0, 1, 1)
        for r in range(90, 91):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._rx_gain_range = Range(0, 50, 1, 5, 200)
        self._rx_gain_win = RangeWidget(self._rx_gain_range, self.set_rx_gain, "'rx_gain'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._rx_gain_win, 96, 0, 1, 1)
        for r in range(96, 97):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._if_gain_range = Range(0, 50, 1, 30, 200)
        self._if_gain_win = RangeWidget(self._if_gain_range, self.set_if_gain, "if_gain", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._if_gain_win, 97, 0, 1, 1)
        for r in range(97, 98):
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
        self._bb_gain_range = Range(0, 50, 1, 30, 200)
        self._bb_gain_win = RangeWidget(self._bb_gain_range, self.set_bb_gain, "BB", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._bb_gain_win, 98, 0, 1, 1)
        for r in range(98, 99):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.single_pole_iir_filter_xx_0 = filter.single_pole_iir_filter_ff(0.000150, 1)
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            freq, #fc
            samp_rate/2, #bw
            "raw", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0.enable_axis_labels(True)



        labels = ['Raw', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.qwidget(), Qt.QWidget)

        self.top_grid_layout.addWidget(self._qtgui_waterfall_sink_x_0_win, 7, 0, 1, 4)
        for r in range(7, 8):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_1_2_0_0 = qtgui.time_sink_f(
            1024, #size
            samp_rate, #samp_rate
            "Rx", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_1_2_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_1_2_0_0.set_y_axis(-0.5, 0.5)

        self.qtgui_time_sink_x_1_2_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_1_2_0_0.enable_tags(True)
        self.qtgui_time_sink_x_1_2_0_0.set_trigger_mode(qtgui.TRIG_MODE_AUTO, qtgui.TRIG_SLOPE_POS, 0.2, 0, 0, "")
        self.qtgui_time_sink_x_1_2_0_0.enable_autoscale(True)
        self.qtgui_time_sink_x_1_2_0_0.enable_grid(False)
        self.qtgui_time_sink_x_1_2_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_1_2_0_0.enable_control_panel(True)
        self.qtgui_time_sink_x_1_2_0_0.enable_stem_plot(False)


        labels = ['Raw DC Blocked R', 'Raw DC Blocked I', 'dqpsk R', 'dqpsk I', 'Sub i',
            'Sub q', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_1_2_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_1_2_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_1_2_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_1_2_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_1_2_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_1_2_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_1_2_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_1_2_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_1_2_0_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_1_2_0_0_win, 5, 0, 1, 4)
        for r in range(5, 6):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_1_2 = qtgui.time_sink_c(
            1024, #size
            samp_rate, #samp_rate
            "Rx", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_1_2.set_update_time(0.10)
        self.qtgui_time_sink_x_1_2.set_y_axis(-0.5, 0.5)

        self.qtgui_time_sink_x_1_2.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_1_2.enable_tags(True)
        self.qtgui_time_sink_x_1_2.set_trigger_mode(qtgui.TRIG_MODE_AUTO, qtgui.TRIG_SLOPE_POS, 0.2, 0, 0, "")
        self.qtgui_time_sink_x_1_2.enable_autoscale(True)
        self.qtgui_time_sink_x_1_2.enable_grid(False)
        self.qtgui_time_sink_x_1_2.enable_axis_labels(True)
        self.qtgui_time_sink_x_1_2.enable_control_panel(True)
        self.qtgui_time_sink_x_1_2.enable_stem_plot(False)


        labels = ['Raw DC Blocked R', 'Raw DC Blocked I', 'dqpsk R', 'dqpsk I', 'Sub i',
            'Sub q', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_1_2.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_1_2.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_1_2.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_1_2.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_1_2.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_1_2.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_1_2.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_1_2.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_1_2_win = sip.wrapinstance(self.qtgui_time_sink_x_1_2.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_1_2_win, 8, 0, 1, 4)
        for r in range(8, 9):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
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
        self.osmosdr_source_0 = osmosdr.source(
            args="numchan=" + str(1) + " " + 'hackrf'
        )
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(freq, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(2, 0)
        self.osmosdr_source_0.set_iq_balance_mode(2, 0)
        self.osmosdr_source_0.set_gain_mode(True, 0)
        self.osmosdr_source_0.set_gain(rx_gain, 0)
        self.osmosdr_source_0.set_if_gain(if_gain, 0)
        self.osmosdr_source_0.set_bb_gain(bb_gain, 0)
        self.osmosdr_source_0.set_antenna('LNAH', 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            245,
            firdes.low_pass(
                1,
                samp_rate,
                100000,
                25000,
                window.WIN_HAMMING,
                6.76))
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
        self._channel_options = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]
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
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_sub_xx_0 = blocks.sub_ff(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_file_sink_0_0_1_0 = blocks.file_sink(gr.sizeof_char*1, '/opt/gr-wban/wpan.pcap', False)
        self.blocks_file_sink_0_0_1_0.set_unbuffered(True)
        self.analog_simple_squelch_cc_0 = analog.simple_squelch_cc(-20, 1)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_SIN_WAVE, 1000000, 5, 0, 0)
        self.analog_quadrature_demod_cf_0 = analog.quadrature_demod_cf(1)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.ieee802_15_4_packet_sink_0, 'out'), (self.foo_wireshark_connector_0, 'in'))
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.blocks_sub_xx_0, 0))
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.single_pole_iir_filter_xx_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.analog_simple_squelch_cc_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_sub_xx_0, 0), (self.digital_clock_recovery_mm_xx_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.digital_clock_recovery_mm_xx_0, 0), (self.digital_symbol_sync_xx_0, 0))
        self.connect((self.digital_symbol_sync_xx_0, 0), (self.ieee802_15_4_packet_sink_0, 0))
        self.connect((self.foo_wireshark_connector_0, 0), (self.blocks_file_sink_0_0_1_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.analog_quadrature_demod_cf_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.qtgui_const_sink_x_1_1, 0))
        self.connect((self.low_pass_filter_0, 0), (self.qtgui_time_sink_x_1_2, 0))
        self.connect((self.low_pass_filter_0, 0), (self.qtgui_waterfall_sink_x_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.analog_simple_squelch_cc_0, 0))
        self.connect((self.single_pole_iir_filter_xx_0, 0), (self.blocks_sub_xx_0, 1))
        self.connect((self.single_pole_iir_filter_xx_0, 0), (self.qtgui_time_sink_x_1_2_0_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "ieee802154_transceiver")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_channel(self):
        return self.channel

    def set_channel(self, channel):
        self.channel = channel
        self._channel_callback(self.channel)
        self.set_freq(2405000000 + 5000000*(self.channel - 11))

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.set_freq_label(self.freq / 1000000000.0)
        self.osmosdr_source_0.set_center_freq(self.freq, 0)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.freq, self.samp_rate/2)

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
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 100000, 25000, window.WIN_HAMMING, 6.76))
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)
        self.qtgui_time_sink_x_1_2.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_1_2_0_0.set_samp_rate(self.samp_rate)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.freq, self.samp_rate/2)

    def get_rx_gain(self):
        return self.rx_gain

    def set_rx_gain(self, rx_gain):
        self.rx_gain = rx_gain
        self.osmosdr_source_0.set_gain(self.rx_gain, 0)

    def get_page_label(self):
        return self.page_label

    def set_page_label(self, page_label):
        self.page_label = page_label
        Qt.QMetaObject.invokeMethod(self._page_label_label, "setText", Qt.Q_ARG("QString", str(self._page_label_formatter(self.page_label))))

    def get_if_gain(self):
        return self.if_gain

    def set_if_gain(self, if_gain):
        self.if_gain = if_gain
        self.osmosdr_source_0.set_if_gain(self.if_gain, 0)

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
        self.osmosdr_source_0.set_bb_gain(self.bb_gain, 0)




def main(top_block_cls=ieee802154_transceiver, options=None):
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print("Error: failed to enable real-time scheduling.")

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
