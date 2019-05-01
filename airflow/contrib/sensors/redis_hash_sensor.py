# -*- coding: utf-8 -*-
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
from airflow.contrib.hooks.redis_hook import RedisHook
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.utils.decorators import apply_defaults


class RedisHashSensor(BaseSensorOperator):
    """
    Checks for the existence of a key in a hash in Redis
    """
    template_fields = ('key', 'hash', )
    ui_color = '#f0eee4'

    @apply_defaults
    def __init__(self, key, hash, redis_conn_id, *args, **kwargs):
        super(RedisHashSensor, self).__init__(*args, **kwargs)
        self.redis_conn_id = redis_conn_id
        self.hash = hash
        self.key = key

    def poke(self, context):
        self.log.info('Sensor checks for existence of key: %s in %s', self.key, self.hash)
        return RedisHook(self.redis_conn_id).get_conn().hexists(self.hash, self.key)
