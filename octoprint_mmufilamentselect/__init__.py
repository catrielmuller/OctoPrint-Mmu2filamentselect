# coding=utf-8
from __future__ import absolute_import
import octoprint.plugin
from threading import Timer

from octoprint.server import user_permission

import flask
from flask_babel import gettext

import octoprint_mmufilamentselect.versions

class MMUSelectPlugin(octoprint.plugin.TemplatePlugin, octoprint.plugin.SettingsPlugin, octoprint.plugin.SimpleApiPlugin, octoprint.plugin.AssetPlugin):

	def __init__(self):
		self._active = False
		self._timer = None
		self._timeout = 0;
		self._version = 'MMU1';

	def initialize(self):
		self._timeout = self._settings.get([b"timeout"])
		self._version = self._settings.get([b"version"])
		self._settings.set([b"cmd"], versions.config[self._version]['cmd'])
		self._settings.set([b"tools"], versions.config[self._version]['tools'])

	#~ queuing handling

	def gcode_queuing_handler(self, comm_instance, phase, cmd, cmd_type, gcode, subcode=None, tags=None, *args, **kwargs):
		if cmd != versions.config[self._version]['cmd']:
			return

		if "mmuPlugin:choose_filament_resend" in tags:
			return

		if self._printer.set_job_on_hold(True):
			self._show_prompt()

		return None,

	#~ SettingsPlugin

	def get_settings_defaults(self):
		return dict(
			timeout=30,
			version="MMU1",
			cmd=versions.config['MMU1']['cmd'],
			tools=versions.config['MMU1']['tools']
		)

	def on_settings_save(self, data):
		try:
			data[b"timeout"]=int(data[b"timeout"])
		except:
			data[b"timeout"]=30

		if data[b"timeout"] < 0:
			data[b"timeout"]=30

		octoprint.plugin.SettingsPlugin.on_settings_save(self, data)
		self._timeout = self._settings.get([b"timeout"])
		self._version = self._settings.get([b"version"])
		self._settings.set([b"cmd"], versions.config[self._version]['cmd'])
		self._settings.set([b"tools"], versions.config[self._version]['tools'])

	#~ TemplatePlugin

	def get_template_configs(self):
		return [
			dict(type="settings", name=gettext("MMU Select Filament"), custom_bindings=False)
		]

	#~ AssetPlugin

	def get_assets(self):
		return dict(
			js=["js/mmufilamentselect.js"]
		)

	#~ prompt handling

	def _show_prompt(self):
		self._active = True
		self._timer = Timer(float(self._timeout), self._timeout_prompt)
		self._timer.start()
		self._plugin_manager.send_plugin_message(self._identifier, dict(action="show"))

	def _timeout_prompt(self):
		self._plugin_manager.send_plugin_message(self._identifier, dict(action="close"))
		self._done_prompt(versions.config[self._version]['cmd'], tags={"mmuPlugin:choose_filament_resend"})

	def _done_prompt(self, command, tags=set()):
		self._timer.cancel()
		self._active = False
		self._printer.commands(command, tags=tags)
		self._printer.set_job_on_hold(False)

	#~ SimpleApiPlugin

	def get_api_commands(self):
		return dict(select=["choice"])

	def on_api_command(self, command, data):
		if command == "select":
			if not user_permission.can():
				return flask.abort(403, "Insufficient permissions")

			if self._active is False:
				return flask.abort(409, "No active prompt")

			choice = data["choice"]
			if not isinstance(choice, int) or not choice < versions.config[self._version]['tools'] or not choice >= 0:
				return flask.abort(400, "{!r} is not a valid value for filament choice".format(choice+1))

			self._done_prompt("T" + str(choice))

	#~ Update

	def get_update_information(*args, **kwargs):
		return dict(
			mmufilamentselect=dict(
				displayName=self._plugin_name,
				displayVersion=self._plugin_version,
				type="github_release",
				current=self._plugin_version,
				user="derPicknicker1",
				repo="OctoPrint-Mmu2filamentselect",
				pip="https://github.com/derPicknicker1/OctoPrint-Mmu2filamentselect/archive/{target_version}.zip"
			)
		)


__plugin_name__ = "Prusa MMU Select Filament"
__plugin_implementation__ = MMUSelectPlugin()
__plugin_hooks__ = {
	b"octoprint.comm.protocol.gcode.queuing": __plugin_implementation__.gcode_queuing_handler,
	b"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
}
