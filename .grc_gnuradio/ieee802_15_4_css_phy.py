# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: IEEE 802.15.4 CSS PHY
# Author: Felix Wunsch
# Description: IEEE 802.15.4 CSS PHY
# GNU Radio version: 3.9.8.0

from gnuradio import blocks
from gnuradio import digital
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
import ieee802_15_4
import math
import numpy as np







class ieee802_15_4_css_phy(gr.hier_block2):
    def __init__(self, bits_per_cw=1, chirp_seq=[], codewords=[[0,0],[1,1]], intlv_seq=[], len_sub=1, nbytes_payload=127, nsamp_frame=1, num_subchirps=1, nzeros_padding=0, phr=[0 for i in range(12)], preamble=(), sfd=(), sym_per_frame=1, threshold=0, time_gap_1=(), time_gap_2=()):
        gr.hier_block2.__init__(
            self, "IEEE 802.15.4 CSS PHY",
                gr.io_signature(1, 1, gr.sizeof_gr_complex*1),
                gr.io_signature.makev(5, 5, [gr.sizeof_gr_complex*1, gr.sizeof_gr_complex*1, gr.sizeof_gr_complex*1, gr.sizeof_gr_complex*1, gr.sizeof_gr_complex*1]),
        )
        self.message_port_register_hier_in("txin")
        self.message_port_register_hier_out("rxout")

        ##################################################
        # Parameters
        ##################################################
        self.bits_per_cw = bits_per_cw
        self.chirp_seq = chirp_seq
        self.codewords = codewords
        self.intlv_seq = intlv_seq
        self.len_sub = len_sub
        self.nbytes_payload = nbytes_payload
        self.nsamp_frame = nsamp_frame
        self.num_subchirps = num_subchirps
        self.nzeros_padding = nzeros_padding
        self.phr = phr
        self.preamble = preamble
        self.sfd = sfd
        self.sym_per_frame = sym_per_frame
        self.threshold = threshold
        self.time_gap_1 = time_gap_1
        self.time_gap_2 = time_gap_2

        ##################################################
        # Blocks
        ##################################################
        self.ieee802_15_4_zeropadding_removal_b_0_0 = ieee802_15_4.zeropadding_removal_b(nbytes_payload*8+len(phr), nzeros_padding)
        self.ieee802_15_4_zeropadding_b_0 = ieee802_15_4.zeropadding_b(nzeros_padding)
        self.ieee802_15_4_qpsk_mapper_if_0 = ieee802_15_4.qpsk_mapper_if()
        self.ieee802_15_4_preamble_tagger_cc_0 = ieee802_15_4.preamble_tagger_cc(len(preamble))
        self.ieee802_15_4_preamble_sfd_prefixer_ii_0_0 = ieee802_15_4.preamble_sfd_prefixer_ii(preamble, sfd, sym_per_frame)
        self.ieee802_15_4_preamble_sfd_prefixer_ii_0 = ieee802_15_4.preamble_sfd_prefixer_ii(preamble, sfd, sym_per_frame)
        self.ieee802_15_4_phr_removal_0_0 = ieee802_15_4.phr_removal(phr)
        self.ieee802_15_4_phr_prefixer_0 = ieee802_15_4.phr_prefixer(phr)
        self.ieee802_15_4_multiuser_chirp_detector_cc_0 = ieee802_15_4.multiuser_chirp_detector_cc(chirp_seq, len(time_gap_1), len(time_gap_2), len_sub, threshold)
        self.ieee802_15_4_interleaver_ii_0_0 = ieee802_15_4.interleaver_ii(intlv_seq, True)
        self.ieee802_15_4_interleaver_ii_0 = ieee802_15_4.interleaver_ii(intlv_seq, True)
        self.ieee802_15_4_frame_buffer_cc_0 = ieee802_15_4.frame_buffer_cc(sym_per_frame)
        self.ieee802_15_4_dqpsk_soft_demapper_cc_0 = ieee802_15_4.dqpsk_soft_demapper_cc(sym_per_frame)
        self.ieee802_15_4_dqpsk_mapper_ff_0 = ieee802_15_4.dqpsk_mapper_ff(sym_per_frame, True)
        self.ieee802_15_4_dqcsk_mapper_fc_0 = ieee802_15_4.dqcsk_mapper_fc(chirp_seq, time_gap_1, time_gap_2, len_sub, num_subchirps, sym_per_frame)
        self.ieee802_15_4_deinterleaver_ff_0_0 = ieee802_15_4.deinterleaver_ff(intlv_seq)
        self.ieee802_15_4_deinterleaver_ff_0 = ieee802_15_4.deinterleaver_ff(intlv_seq)
        self.ieee802_15_4_codeword_soft_demapper_fb_0_0 = ieee802_15_4.codeword_soft_demapper_fb(bits_per_cw, codewords)
        self.ieee802_15_4_codeword_soft_demapper_fb_0 = ieee802_15_4.codeword_soft_demapper_fb(bits_per_cw, codewords)
        self.ieee802_15_4_codeword_mapper_bi_0_0 = ieee802_15_4.codeword_mapper_bi(bits_per_cw, codewords)
        self.ieee802_15_4_codeword_mapper_bi_0 = ieee802_15_4.codeword_mapper_bi(bits_per_cw, codewords)
        self.digital_costas_loop_cc_0 = digital.costas_loop_cc(2 * math.pi / 100, 4, False)
        self.blocks_stream_to_tagged_stream_0 = blocks.stream_to_tagged_stream(gr.sizeof_gr_complex, 1, nsamp_frame, "burst_len")
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_cc(np.exp(1j*np.pi/4))
        self.blocks_keep_m_in_n_0_0_0_0 = blocks.keep_m_in_n(gr.sizeof_float, sym_per_frame-len(preamble)-len(sfd), sym_per_frame, len(preamble)+len(sfd))
        self.blocks_keep_m_in_n_0_0_0 = blocks.keep_m_in_n(gr.sizeof_float, sym_per_frame-len(preamble)-len(sfd), sym_per_frame, len(preamble)+len(sfd))
        self.blocks_interleave_0_0 = blocks.interleave(gr.sizeof_char*1, 1)
        self.blocks_deinterleave_0 = blocks.deinterleave(gr.sizeof_char*1, 1)
        self.blocks_complex_to_float_0 = blocks.complex_to_float(1)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.ieee802_15_4_phr_prefixer_0, 'out'), (self.ieee802_15_4_zeropadding_b_0, 'in'))
        self.msg_connect((self.ieee802_15_4_phr_removal_0_0, 'out'), (self, 'rxout'))
        self.msg_connect((self.ieee802_15_4_zeropadding_removal_b_0_0, 'out'), (self.ieee802_15_4_phr_removal_0_0, 'in'))
        self.msg_connect((self, 'txin'), (self.ieee802_15_4_phr_prefixer_0, 'in'))
        self.connect((self.blocks_complex_to_float_0, 0), (self.blocks_keep_m_in_n_0_0_0, 0))
        self.connect((self.blocks_complex_to_float_0, 1), (self.blocks_keep_m_in_n_0_0_0_0, 0))
        self.connect((self.blocks_deinterleave_0, 0), (self.ieee802_15_4_codeword_mapper_bi_0, 0))
        self.connect((self.blocks_deinterleave_0, 1), (self.ieee802_15_4_codeword_mapper_bi_0_0, 0))
        self.connect((self.blocks_interleave_0_0, 0), (self.ieee802_15_4_zeropadding_removal_b_0_0, 0))
        self.connect((self.blocks_keep_m_in_n_0_0_0, 0), (self.ieee802_15_4_deinterleaver_ff_0, 0))
        self.connect((self.blocks_keep_m_in_n_0_0_0_0, 0), (self.ieee802_15_4_deinterleaver_ff_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_complex_to_float_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self, 4))
        self.connect((self.blocks_stream_to_tagged_stream_0, 0), (self, 0))
        self.connect((self.digital_costas_loop_cc_0, 0), (self.ieee802_15_4_preamble_tagger_cc_0, 0))
        self.connect((self.digital_costas_loop_cc_0, 0), (self, 2))
        self.connect((self.ieee802_15_4_codeword_mapper_bi_0, 0), (self.ieee802_15_4_interleaver_ii_0, 0))
        self.connect((self.ieee802_15_4_codeword_mapper_bi_0_0, 0), (self.ieee802_15_4_interleaver_ii_0_0, 0))
        self.connect((self.ieee802_15_4_codeword_soft_demapper_fb_0, 0), (self.blocks_interleave_0_0, 1))
        self.connect((self.ieee802_15_4_codeword_soft_demapper_fb_0_0, 0), (self.blocks_interleave_0_0, 0))
        self.connect((self.ieee802_15_4_deinterleaver_ff_0, 0), (self.ieee802_15_4_codeword_soft_demapper_fb_0_0, 0))
        self.connect((self.ieee802_15_4_deinterleaver_ff_0_0, 0), (self.ieee802_15_4_codeword_soft_demapper_fb_0, 0))
        self.connect((self.ieee802_15_4_dqcsk_mapper_fc_0, 0), (self.blocks_stream_to_tagged_stream_0, 0))
        self.connect((self.ieee802_15_4_dqpsk_mapper_ff_0, 0), (self.ieee802_15_4_dqcsk_mapper_fc_0, 0))
        self.connect((self.ieee802_15_4_dqpsk_soft_demapper_cc_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.ieee802_15_4_frame_buffer_cc_0, 0), (self.ieee802_15_4_dqpsk_soft_demapper_cc_0, 0))
        self.connect((self.ieee802_15_4_frame_buffer_cc_0, 0), (self, 3))
        self.connect((self.ieee802_15_4_interleaver_ii_0, 0), (self.ieee802_15_4_preamble_sfd_prefixer_ii_0, 0))
        self.connect((self.ieee802_15_4_interleaver_ii_0_0, 0), (self.ieee802_15_4_preamble_sfd_prefixer_ii_0_0, 0))
        self.connect((self.ieee802_15_4_multiuser_chirp_detector_cc_0, 0), (self.digital_costas_loop_cc_0, 0))
        self.connect((self.ieee802_15_4_multiuser_chirp_detector_cc_0, 0), (self, 1))
        self.connect((self.ieee802_15_4_preamble_sfd_prefixer_ii_0, 0), (self.ieee802_15_4_qpsk_mapper_if_0, 1))
        self.connect((self.ieee802_15_4_preamble_sfd_prefixer_ii_0_0, 0), (self.ieee802_15_4_qpsk_mapper_if_0, 0))
        self.connect((self.ieee802_15_4_preamble_tagger_cc_0, 0), (self.ieee802_15_4_frame_buffer_cc_0, 0))
        self.connect((self.ieee802_15_4_qpsk_mapper_if_0, 0), (self.ieee802_15_4_dqpsk_mapper_ff_0, 0))
        self.connect((self.ieee802_15_4_zeropadding_b_0, 0), (self.blocks_deinterleave_0, 0))
        self.connect((self, 0), (self.ieee802_15_4_multiuser_chirp_detector_cc_0, 0))


    def get_bits_per_cw(self):
        return self.bits_per_cw

    def set_bits_per_cw(self, bits_per_cw):
        self.bits_per_cw = bits_per_cw

    def get_chirp_seq(self):
        return self.chirp_seq

    def set_chirp_seq(self, chirp_seq):
        self.chirp_seq = chirp_seq

    def get_codewords(self):
        return self.codewords

    def set_codewords(self, codewords):
        self.codewords = codewords

    def get_intlv_seq(self):
        return self.intlv_seq

    def set_intlv_seq(self, intlv_seq):
        self.intlv_seq = intlv_seq

    def get_len_sub(self):
        return self.len_sub

    def set_len_sub(self, len_sub):
        self.len_sub = len_sub

    def get_nbytes_payload(self):
        return self.nbytes_payload

    def set_nbytes_payload(self, nbytes_payload):
        self.nbytes_payload = nbytes_payload

    def get_nsamp_frame(self):
        return self.nsamp_frame

    def set_nsamp_frame(self, nsamp_frame):
        self.nsamp_frame = nsamp_frame
        self.blocks_stream_to_tagged_stream_0.set_packet_len(self.nsamp_frame)
        self.blocks_stream_to_tagged_stream_0.set_packet_len_pmt(self.nsamp_frame)

    def get_num_subchirps(self):
        return self.num_subchirps

    def set_num_subchirps(self, num_subchirps):
        self.num_subchirps = num_subchirps

    def get_nzeros_padding(self):
        return self.nzeros_padding

    def set_nzeros_padding(self, nzeros_padding):
        self.nzeros_padding = nzeros_padding

    def get_phr(self):
        return self.phr

    def set_phr(self, phr):
        self.phr = phr

    def get_preamble(self):
        return self.preamble

    def set_preamble(self, preamble):
        self.preamble = preamble
        self.blocks_keep_m_in_n_0_0_0.set_offset(len(self.preamble)+len(self.sfd))
        self.blocks_keep_m_in_n_0_0_0.set_m(self.sym_per_frame-len(self.preamble)-len(self.sfd))
        self.blocks_keep_m_in_n_0_0_0_0.set_offset(len(self.preamble)+len(self.sfd))
        self.blocks_keep_m_in_n_0_0_0_0.set_m(self.sym_per_frame-len(self.preamble)-len(self.sfd))

    def get_sfd(self):
        return self.sfd

    def set_sfd(self, sfd):
        self.sfd = sfd
        self.blocks_keep_m_in_n_0_0_0.set_offset(len(self.preamble)+len(self.sfd))
        self.blocks_keep_m_in_n_0_0_0.set_m(self.sym_per_frame-len(self.preamble)-len(self.sfd))
        self.blocks_keep_m_in_n_0_0_0_0.set_offset(len(self.preamble)+len(self.sfd))
        self.blocks_keep_m_in_n_0_0_0_0.set_m(self.sym_per_frame-len(self.preamble)-len(self.sfd))

    def get_sym_per_frame(self):
        return self.sym_per_frame

    def set_sym_per_frame(self, sym_per_frame):
        self.sym_per_frame = sym_per_frame
        self.blocks_keep_m_in_n_0_0_0.set_m(self.sym_per_frame-len(self.preamble)-len(self.sfd))
        self.blocks_keep_m_in_n_0_0_0.set_n(self.sym_per_frame)
        self.blocks_keep_m_in_n_0_0_0_0.set_m(self.sym_per_frame-len(self.preamble)-len(self.sfd))
        self.blocks_keep_m_in_n_0_0_0_0.set_n(self.sym_per_frame)

    def get_threshold(self):
        return self.threshold

    def set_threshold(self, threshold):
        self.threshold = threshold

    def get_time_gap_1(self):
        return self.time_gap_1

    def set_time_gap_1(self, time_gap_1):
        self.time_gap_1 = time_gap_1

    def get_time_gap_2(self):
        return self.time_gap_2

    def set_time_gap_2(self, time_gap_2):
        self.time_gap_2 = time_gap_2

