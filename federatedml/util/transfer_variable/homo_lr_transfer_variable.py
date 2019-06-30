#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from federatedml.util.transfer_variable.base_transfer_variable import BaseTransferVariable, Variable


class HomoLRTransferVariable(BaseTransferVariable):
    def define_transfer_variable(self):
        self.paillier_pubkey = Variable(name="HomoLRTransferVariable.paillier_pubkey", auth={'src': "arbiter", 'dst': ['host']})
        self.guest_model = Variable(name="HomoLRTransferVariable.guest_model", auth={'src': "guest", 'dst': ['arbiter']})
        self.host_model = Variable(name="HomoLRTransferVariable.host_model", auth={'src': "host", 'dst': ['arbiter']})
        self.final_model = Variable(name="HomoLRTransferVariable.final_model", auth={'src': "arbiter", 'dst': ['guest', 'host']})
        self.to_encrypt_model = Variable(name="HomoLRTransferVariable.to_encrypt_model", auth={'src': "host", 'dst': ['arbiter']})
        self.re_encrypted_model = Variable(name="HomoLRTransferVariable.re_encrypted_model", auth={'src': "arbiter", 'dst': ['host']})
        self.re_encrypt_times = Variable(name="HomoLRTransferVariable.re_encrypt_times", auth={'src': "host", 'dst': ['arbiter']})
        self.converge_flag = Variable(name="HomoLRTransferVariable.converge_flag", auth={'src': "arbiter", 'dst': ['guest', 'host']})
        self.guest_loss = Variable(name="HomoLRTransferVariable.guest_loss", auth={'src': "guest", 'dst': ['arbiter']})
        self.host_loss = Variable(name="HomoLRTransferVariable.host_loss", auth={'src': "host", 'dst': ['arbiter']})
        self.use_encrypt = Variable(name="HomoLRTransferVariable.use_encrypt", auth={'src': "host", 'dst': ['arbiter']})
        self.guest_party_weight = Variable(name="HomoLRTransferVariable.guest_party_weight", auth={'src': "guest", 'dst': ['arbiter']})
        self.host_party_weight = Variable(name="HomoLRTransferVariable.host_party_weight", auth={'src': "host", 'dst': ['arbiter']})
        self.predict_wx = Variable(name="HomoLRTransferVariable.predict_wx", auth={'src': "host", 'dst': ['arbiter']})
        self.predict_result = Variable(name="HomoLRTransferVariable.predict_result", auth={'src': "arbiter", 'dst': ['host']})
        pass