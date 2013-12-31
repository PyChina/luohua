#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 落花 / 数据结构 / 虚线索池
#
# Copyright (C) 2013 JNRain
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals, division

import six

from weiyu.db.mapper import mapper_hub
from weiyu.db.mapper.base import Document

VTP_STRUCT_ID = 'luohua.vtp'
mapper_hub.register_struct(VTP_STRUCT_ID)


class VPool(Document):
    '''虚线索池.

    本结构的存储后端应为 Riak.

    .. note::
        ``VPool`` 的简称取成 ``vtp`` 而不是 ``vp`` 的原因是 ``vp``
        会和视频编码算法 VP 系列冲突.

    '''

    struct_id = VTP_STRUCT_ID

    def __init__(self, data=None, vtpid=None, rawobj=None):
        super(VPool, self).__init__()

        if data is not None:
            self.update(self.decode(data))

        if vtpid is not None:
            self['id'] = vtpid

        self._rawobj = rawobj

    @classmethod
    def _from_obj(cls, obj):
        return cls(obj.data, obj.key, obj) if obj.exists else None

    @classmethod
    def find(cls, vtpid):
        '''按文档 ID 获取一个虚线索池.'''

        with cls.storage as conn:
            obj = conn.get(vtpid)
            return cls._from_obj(obj)

    @classmethod
    def find_all(cls):
        '''一次性获取所有虚线索池.'''

        with cls.storage as conn:
            for vtpid in conn.get_keys():
                obj = conn.get(vtpid)
                yield cls._from_obj(obj)

    def save(self):
        '''保存虚线索池到数据库.'''

        with self.storage as conn:
            obj = self._rawobj if self._rawobj is not None else conn.new()

            # 文档 ID 未指定则自动生成
            obj.key, obj.data = self.get('id'), self.encode()

            obj.store()

            # 刷新对象关联信息
            self['id'], self._rawobj = obj.key, obj


@mapper_hub.decoder_for(VTP_STRUCT_ID, 1)
def vtp_dec_v1(data):
    return {
            'name': data['n'],
            'natural': data['t'],
            'xattr': data['x'],
            }


@mapper_hub.encoder_for(VTP_STRUCT_ID, 1)
def vtp_enc_v1(vtp):
    assert 'name' in vtp
    assert isinstance(vtp['name'], six.text_type)
    assert 'natural' in vtp
    assert isinstance(vtp['natural'], bool)
    assert 'xattr' in vtp
    assert isinstance(vtp['xattr'], dict)

    return {
            'n': vtp['name'],
            't': vtp['natural'],
            'x': vtp['xattr'],
            }


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
