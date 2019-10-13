(function (global, factory) {
    if (typeof define === "function" && define.amd) {
        define(["OctoPrintClient"], factory);
    } else {
        factory(global.OctoPrintClient);
    }
})(this, function(OctoPrintClient) {
    var OctoPrintMMUSelect = function(base) {
        this.base = base;
    };

    OctoPrintMMUSelect.prototype.select = function(index, opts) {
        var data = {
            choice: index
        };
        return this.base.simpleApiCommand("mmufilamentselect", "select", data, opts);
    };

    OctoPrintClient.registerPluginComponent("mmufilamentselect", OctoPrintMMUSelect);
    return OctoPrintMMUSelect;
});

$(function() {
    function MMUSelectViewModel(parameters) {
        var self = this;

        self.settings = parameters[0];
        self.loginState = parameters[1];

        self._modal = undefined;

        self._showPrompt = function() {
            var tools = self.settings.settings.plugins.mmufilamentselect.tools();
            var selections = {};
            for (var i = 0; i < tools; i += 1) {
                selections[i] = 'Filament ' + (i + 1);
            }
            var opts = {
                title: gettext("Prusa MMU filament select"),
                message: gettext("Select the filament spool you wish to use for this single color print."),
                selections: selections,
                onselect: function(index) {
                    if (index > -1) {
                        self._select(index);
                    }
                },
                onclose: function() {
                    self._modal = undefined;
                }
            };
            self._modal = showSelectionDialog(opts)
            setTimeout(self._closePrompt, self.settings.settings.plugins.mmufilamentselect.timeout() * 1000);
        };

        self._select = function(index) {
            OctoPrint.plugins.mmufilamentselect.select(index);
        };

        self._closePrompt = function() {
            if (self._modal) {
                self._modal.modal("hide");
            }
        };

        self.onDataUpdaterPluginMessage = function(plugin, data) {
            if (!self.loginState.isUser()) return;
            if (plugin !== "mmufilamentselect") {
                return;
            }
            switch (data.action) {
                case "show": {
                    self._showPrompt();
                    break;
                }
                case "close": {
                    self._closePrompt();
                    break;
                }
            }
        }

    }

    OCTOPRINT_VIEWMODELS.push({
        construct: MMUSelectViewModel,
        dependencies: ["settingsViewModel","loginStateViewModel"]
    });
});
