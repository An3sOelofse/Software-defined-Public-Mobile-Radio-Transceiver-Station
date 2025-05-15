#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Walkie Talkie
# GNU Radio version: 3.10.9.2

from PyQt5 import Qt
from gnuradio import qtgui
import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from PyQt5 import QtCore
from PyQt5.QtCore import QObject, pyqtSlot
from dcss_generation import dcss_generation  # grc-generated hier_block
from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import digital
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time
from pmr_channel_demod import pmr_channel_demod  # grc-generated hier_block
import pmr_walkie_talkie_epy_block_0 as epy_block_0  # embedded python block
import pmr_walkie_talkie_epy_block_1 as epy_block_1  # embedded python block
import sip



class pmr_walkie_talkie(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Walkie Talkie", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Walkie Talkie")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
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

        self.settings = Qt.QSettings("GNU Radio", "pmr_walkie_talkie")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.tuning = tuning = 446000000
        self.selected_channel = selected_channel = 1
        self.selected_DCS = selected_DCS = 1
        self.samp_rate = samp_rate = 384000
        self.rf_gain_tx = rf_gain_tx = 60
        self.rf_gain = rf_gain = 30
        self.PTT = PTT = 0
        self.DCS = DCS = 1

        ##################################################
        # Blocks
        ##################################################

        # Create the options list
        self._selected_channel_options = [1, 2, 3, 4, 5, 6, 7, 8]
        # Create the labels list
        self._selected_channel_labels = ['Channel 1', 'Channel 2', 'Channel 3', 'Channel 4', 'Channel 5', 'Channel 6', 'Channel 7', 'Channel 8']
        # Create the combo box
        # Create the radio buttons
        self._selected_channel_group_box = Qt.QGroupBox("Channel" + ": ")
        self._selected_channel_box = Qt.QHBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._selected_channel_button_group = variable_chooser_button_group()
        self._selected_channel_group_box.setLayout(self._selected_channel_box)
        for i, _label in enumerate(self._selected_channel_labels):
            radio_button = Qt.QRadioButton(_label)
            self._selected_channel_box.addWidget(radio_button)
            self._selected_channel_button_group.addButton(radio_button, i)
        self._selected_channel_callback = lambda i: Qt.QMetaObject.invokeMethod(self._selected_channel_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._selected_channel_options.index(i)))
        self._selected_channel_callback(self.selected_channel)
        self._selected_channel_button_group.buttonClicked[int].connect(
            lambda i: self.set_selected_channel(self._selected_channel_options[i]))
        self.top_layout.addWidget(self._selected_channel_group_box)
        self._rf_gain_tx_range = qtgui.Range(0, 76, 1, 60, 200)
        self._rf_gain_tx_win = qtgui.RangeWidget(self._rf_gain_tx_range, self.set_rf_gain_tx, "Transmit Gain", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._rf_gain_tx_win)
        self._rf_gain_range = qtgui.Range(0, 76, 1, 30, 200)
        self._rf_gain_win = qtgui.RangeWidget(self._rf_gain_range, self.set_rf_gain, "RF Gain", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._rf_gain_win)
        _PTT_push_button = Qt.QPushButton('Push To Talk')
        _PTT_push_button = Qt.QPushButton('Push To Talk')
        self._PTT_choices = {'Pressed': 1, 'Released': 0}
        _PTT_push_button.pressed.connect(lambda: self.set_PTT(self._PTT_choices['Pressed']))
        _PTT_push_button.released.connect(lambda: self.set_PTT(self._PTT_choices['Released']))
        self.top_layout.addWidget(_PTT_push_button)
        self._DCS_choices = {'Pressed': 1, 'Released': 0}

        _DCS_toggle_button = qtgui.ToggleButton(self.set_DCS, 'DCS', self._DCS_choices, True, 'value')
        _DCS_toggle_button.setColors("gray", "white", "green", "white")
        self.DCS = _DCS_toggle_button

        self.top_layout.addWidget(_DCS_toggle_button)
        self.uhd_usrp_source_0 = uhd.usrp_source(
            ",".join(("", '')),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
        )
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        # No synchronization enforced.

        self.uhd_usrp_source_0.set_center_freq(tuning, 0)
        self.uhd_usrp_source_0.set_antenna("RX2", 0)
        self.uhd_usrp_source_0.set_bandwidth(200000, 0)
        self.uhd_usrp_source_0.set_rx_agc(False, 0)
        self.uhd_usrp_source_0.set_gain(rf_gain, 0)
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
            ",".join(("", '')),
            uhd.stream_args(
                cpu_format="fc32",
                otw_format="sc16",
                args='',
                channels=list(range(0,1)),
            ),
            "",
        )
        self.uhd_usrp_sink_0.set_samp_rate(384000)
        self.uhd_usrp_sink_0.set_time_now(uhd.time_spec(time.time()), uhd.ALL_MBOARDS)

        self.uhd_usrp_sink_0.set_center_freq(tuning+6250+(12500*(selected_channel-1)), 0)
        self.uhd_usrp_sink_0.set_antenna("TX/RX", 0)
        self.uhd_usrp_sink_0.set_bandwidth(200000, 0)
        self.uhd_usrp_sink_0.set_gain(rf_gain_tx*PTT-(1-PTT)*30, 0)
        # Create the options list
        self._selected_DCS_options = [0, 1]
        # Create the labels list
        self._selected_DCS_labels = ['OFF', 'D023N']
        # Create the combo box
        self._selected_DCS_tool_bar = Qt.QToolBar(self)
        self._selected_DCS_tool_bar.addWidget(Qt.QLabel("DCS Tone" + ": "))
        self._selected_DCS_combo_box = Qt.QComboBox()
        self._selected_DCS_tool_bar.addWidget(self._selected_DCS_combo_box)
        for _label in self._selected_DCS_labels: self._selected_DCS_combo_box.addItem(_label)
        self._selected_DCS_callback = lambda i: Qt.QMetaObject.invokeMethod(self._selected_DCS_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._selected_DCS_options.index(i)))
        self._selected_DCS_callback(self.selected_DCS)
        self._selected_DCS_combo_box.currentIndexChanged.connect(
            lambda i: self.set_selected_DCS(self._selected_DCS_options[i]))
        # Create the radio buttons
        self.top_layout.addWidget(self._selected_DCS_tool_bar)
        self.qtgui_sink_x_0_1_0_0_0_0_1 = qtgui.sink_c(
            8192, #fftsize
            window.WIN_BLACKMAN_hARRIS, #wintype
            tuning, #fc
            samp_rate, #bw
            "Transmit Spectrum", #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True, #plotconst
            None # parent
        )
        self.qtgui_sink_x_0_1_0_0_0_0_1.set_update_time(1.0/100)
        self._qtgui_sink_x_0_1_0_0_0_0_1_win = sip.wrapinstance(self.qtgui_sink_x_0_1_0_0_0_0_1.qwidget(), Qt.QWidget)

        self.qtgui_sink_x_0_1_0_0_0_0_1.enable_rf_freq(True)

        self.top_layout.addWidget(self._qtgui_sink_x_0_1_0_0_0_0_1_win)
        self.qtgui_sink_x_0_1_0_0_0_0_0 = qtgui.sink_f(
            32768, #fftsize
            window.WIN_BLACKMAN_hARRIS, #wintype
            tuning, #fc
            samp_rate, #bw
            "DCSS Time Series", #name
            False, #plotfreq
            False, #plotwaterfall
            True, #plottime
            False, #plotconst
            None # parent
        )
        self.qtgui_sink_x_0_1_0_0_0_0_0.set_update_time(1.0/100)
        self._qtgui_sink_x_0_1_0_0_0_0_0_win = sip.wrapinstance(self.qtgui_sink_x_0_1_0_0_0_0_0.qwidget(), Qt.QWidget)

        self.qtgui_sink_x_0_1_0_0_0_0_0.enable_rf_freq(True)

        self.top_layout.addWidget(self._qtgui_sink_x_0_1_0_0_0_0_0_win)
        self.qtgui_sink_x_0_1_0_0_0_0 = qtgui.sink_c(
            8192, #fftsize
            window.WIN_BLACKMAN_hARRIS, #wintype
            tuning, #fc
            samp_rate, #bw
            "Receive Spectrum", #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True, #plotconst
            None # parent
        )
        self.qtgui_sink_x_0_1_0_0_0_0.set_update_time(1.0/100)
        self._qtgui_sink_x_0_1_0_0_0_0_win = sip.wrapinstance(self.qtgui_sink_x_0_1_0_0_0_0.qwidget(), Qt.QWidget)

        self.qtgui_sink_x_0_1_0_0_0_0.enable_rf_freq(True)

        self.top_layout.addWidget(self._qtgui_sink_x_0_1_0_0_0_0_win)
        self.pmr_channel_demod_0_1_4 = pmr_channel_demod(
            channel=8,
            samp_rate=samp_rate,
        )
        self.pmr_channel_demod_0_1_3 = pmr_channel_demod(
            channel=7,
            samp_rate=samp_rate,
        )
        self.pmr_channel_demod_0_1_2 = pmr_channel_demod(
            channel=6,
            samp_rate=samp_rate,
        )
        self.pmr_channel_demod_0_1_1 = pmr_channel_demod(
            channel=5,
            samp_rate=samp_rate,
        )
        self.pmr_channel_demod_0_1_0 = pmr_channel_demod(
            channel=4,
            samp_rate=samp_rate,
        )
        self.pmr_channel_demod_0_1 = pmr_channel_demod(
            channel=3,
            samp_rate=samp_rate,
        )
        self.pmr_channel_demod_0_0 = pmr_channel_demod(
            channel=2,
            samp_rate=samp_rate,
        )
        self.pmr_channel_demod_0 = pmr_channel_demod(
            channel=1,
            samp_rate=samp_rate,
        )
        self.mmse_resampler_xx_0 = filter.mmse_resampler_ff(0, 1.997)
        self.low_pass_filter_0_1_0_0_0 = filter.fir_filter_fff(
            1,
            firdes.low_pass(
                1,
                48000,
                150,
                50,
                window.WIN_HAMMING,
                6.76))
        self.low_pass_filter_0_1_0_0 = filter.fir_filter_fff(
            1,
            firdes.low_pass(
                1,
                48000,
                200,
                50,
                window.WIN_HAMMING,
                6.76))
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            1,
            firdes.low_pass(
                1,
                384000,
                6000,
                1000,
                window.WIN_HAMMING,
                6.76))
        self.high_pass_filter_0 = filter.fir_filter_fff(
            1,
            firdes.high_pass(
                1,
                24000,
                300,
                50,
                window.WIN_HAMMING,
                6.76))
        self.epy_block_1 = epy_block_1.blk(selected_dcs_code=1)
        self.epy_block_1.set_min_output_buffer((23*178*4))
        self.epy_block_0 = epy_block_0.blk(selected_source=selected_channel)
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self.dcss_generation_0 = dcss_generation(
            DCS_code_value=0,
            audio_sample_rate=24000,
            dcs_active=DCS,
        )
        self.blocks_sub_xx_0 = blocks.sub_ff(1)
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_ff(((1-PTT)))
        self.blocks_multiply_const_vxx_0_0_0 = blocks.multiply_const_cc(PTT)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(3.3)
        self.blocks_moving_average_xx_0 = blocks.moving_average_ff(20000, (1/20000), 20000, 1)
        self.audio_source_0 = audio.source(48000, 'pipewire', True)
        self.audio_sink_0 = audio.sink(48000, '', True)
        self.analog_nbfm_tx_0 = analog.nbfm_tx(
        	audio_rate=24000,
        	quad_rate=384000,
        	tau=(75e-6),
        	max_dev=2.5e3,
        	fh=(-1.0),
                )


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_nbfm_tx_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.audio_source_0, 0), (self.mmse_resampler_xx_0, 0))
        self.connect((self.blocks_moving_average_xx_0, 0), (self.blocks_sub_xx_0, 1))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.digital_binary_slicer_fb_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.qtgui_sink_x_0_1_0_0_0_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0_0, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.audio_sink_0, 0))
        self.connect((self.blocks_sub_xx_0, 0), (self.low_pass_filter_0_1_0_0_0, 0))
        self.connect((self.dcss_generation_0, 0), (self.analog_nbfm_tx_0, 0))
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.epy_block_1, 1))
        self.connect((self.epy_block_0, 0), (self.epy_block_1, 0))
        self.connect((self.epy_block_0, 0), (self.low_pass_filter_0_1_0_0, 0))
        self.connect((self.epy_block_1, 0), (self.blocks_multiply_const_vxx_1, 0))
        self.connect((self.high_pass_filter_0, 0), (self.dcss_generation_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.blocks_multiply_const_vxx_0_0_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.qtgui_sink_x_0_1_0_0_0_0_1, 0))
        self.connect((self.low_pass_filter_0_1_0_0, 0), (self.blocks_moving_average_xx_0, 0))
        self.connect((self.low_pass_filter_0_1_0_0, 0), (self.blocks_sub_xx_0, 0))
        self.connect((self.low_pass_filter_0_1_0_0_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.mmse_resampler_xx_0, 0), (self.high_pass_filter_0, 0))
        self.connect((self.pmr_channel_demod_0, 0), (self.epy_block_0, 0))
        self.connect((self.pmr_channel_demod_0_0, 0), (self.epy_block_0, 1))
        self.connect((self.pmr_channel_demod_0_1, 0), (self.epy_block_0, 2))
        self.connect((self.pmr_channel_demod_0_1_0, 0), (self.epy_block_0, 3))
        self.connect((self.pmr_channel_demod_0_1_1, 0), (self.epy_block_0, 4))
        self.connect((self.pmr_channel_demod_0_1_2, 0), (self.epy_block_0, 5))
        self.connect((self.pmr_channel_demod_0_1_3, 0), (self.epy_block_0, 6))
        self.connect((self.pmr_channel_demod_0_1_4, 0), (self.epy_block_0, 7))
        self.connect((self.uhd_usrp_source_0, 0), (self.pmr_channel_demod_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.pmr_channel_demod_0_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.pmr_channel_demod_0_1, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.pmr_channel_demod_0_1_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.pmr_channel_demod_0_1_1, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.pmr_channel_demod_0_1_2, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.pmr_channel_demod_0_1_3, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.pmr_channel_demod_0_1_4, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.qtgui_sink_x_0_1_0_0_0_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "pmr_walkie_talkie")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_tuning(self):
        return self.tuning

    def set_tuning(self, tuning):
        self.tuning = tuning
        self.qtgui_sink_x_0_1_0_0_0_0.set_frequency_range(self.tuning, self.samp_rate)
        self.qtgui_sink_x_0_1_0_0_0_0_0.set_frequency_range(self.tuning, self.samp_rate)
        self.qtgui_sink_x_0_1_0_0_0_0_1.set_frequency_range(self.tuning, self.samp_rate)
        self.uhd_usrp_sink_0.set_center_freq(self.tuning+6250+(12500*(self.selected_channel-1)), 0)
        self.uhd_usrp_source_0.set_center_freq(self.tuning, 0)

    def get_selected_channel(self):
        return self.selected_channel

    def set_selected_channel(self, selected_channel):
        self.selected_channel = selected_channel
        self._selected_channel_callback(self.selected_channel)
        self.epy_block_0.selected_source = self.selected_channel
        self.uhd_usrp_sink_0.set_center_freq(self.tuning+6250+(12500*(self.selected_channel-1)), 0)

    def get_selected_DCS(self):
        return self.selected_DCS

    def set_selected_DCS(self, selected_DCS):
        self.selected_DCS = selected_DCS
        self._selected_DCS_callback(self.selected_DCS)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.pmr_channel_demod_0.set_samp_rate(self.samp_rate)
        self.pmr_channel_demod_0_0.set_samp_rate(self.samp_rate)
        self.pmr_channel_demod_0_1.set_samp_rate(self.samp_rate)
        self.pmr_channel_demod_0_1_0.set_samp_rate(self.samp_rate)
        self.pmr_channel_demod_0_1_1.set_samp_rate(self.samp_rate)
        self.pmr_channel_demod_0_1_2.set_samp_rate(self.samp_rate)
        self.pmr_channel_demod_0_1_3.set_samp_rate(self.samp_rate)
        self.pmr_channel_demod_0_1_4.set_samp_rate(self.samp_rate)
        self.qtgui_sink_x_0_1_0_0_0_0.set_frequency_range(self.tuning, self.samp_rate)
        self.qtgui_sink_x_0_1_0_0_0_0_0.set_frequency_range(self.tuning, self.samp_rate)
        self.qtgui_sink_x_0_1_0_0_0_0_1.set_frequency_range(self.tuning, self.samp_rate)
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)

    def get_rf_gain_tx(self):
        return self.rf_gain_tx

    def set_rf_gain_tx(self, rf_gain_tx):
        self.rf_gain_tx = rf_gain_tx
        self.uhd_usrp_sink_0.set_gain(self.rf_gain_tx*self.PTT-(1-self.PTT)*30, 0)

    def get_rf_gain(self):
        return self.rf_gain

    def set_rf_gain(self, rf_gain):
        self.rf_gain = rf_gain
        self.uhd_usrp_source_0.set_gain(self.rf_gain, 0)

    def get_PTT(self):
        return self.PTT

    def set_PTT(self, PTT):
        self.PTT = PTT
        self.blocks_multiply_const_vxx_0_0_0.set_k(self.PTT)
        self.blocks_multiply_const_vxx_1.set_k(((1-self.PTT)))
        self.uhd_usrp_sink_0.set_gain(self.rf_gain_tx*self.PTT-(1-self.PTT)*30, 0)

    def get_DCS(self):
        return self.DCS

    def set_DCS(self, DCS):
        self.DCS = DCS
        self.dcss_generation_0.set_dcs_active(self.DCS)




def main(top_block_cls=pmr_walkie_talkie, options=None):
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        gr.logger("realtime").warn("Error: failed to enable real-time scheduling.")

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
