odoo.define('res.users.shortcut', function(require) {
"use strict";
var Widget = require('web.Widget'),
    WebClient = require('web.WebClient'),
    ActionManager = require('web.ActionManager'),
    core = require('web.core'),
    qweb = core.qweb,
    rpc = require('web.rpc'),
    SystrayMenu = require('web.SystrayMenu'),
    session = require('web.session');

var _t = core._t;

var x_shortcuts = null;
var x_transient_models = [];

var ShortcutMenu = Widget.extend({
    template: 'Systray.ShortcutMenu',
    events: {
        'click .oe_systray_shortcut_setting': '_onSetting',
    },
    init: function() {
        this._super();
        this.on('load', this, this.load);
        this.on('add', this, this.add);
        this.on('display', this, this.display);
        this.on('remove', this, this.remove);
    },
    start: function() {
        var self = this;
        this._super();
        this.trigger('load');
        this.$el.on('click', '.oe_systray_shortcut_menu a', function() {
            self.click($(this));
        });
    },
    _onSetting: function(){
        var self = this;
        rpc.query({
            route: "/web/action/load",
            params: {
                action_id: "web_user_shortcut.actions_web_user_shortcut",
            },
        })
        .done(function (action_id) {
            action_id.res_id = session.uid;
            self.trigger('click_setting', action_id);
        });
    },
    load: function() {
        var self = this;
        this.$el.find('.oe_systray_shortcut_menu li').remove();
        return rpc.query({
            model: 'res.users.shortcut',
            method: 'get_shortcut_data',
            args: [],
        }).done(function(res) {
            var shortcuts = res.shortcuts;
            x_transient_models = res.transient_models;
            if (!shortcuts.length) {
                self.$el.hide();
            }
            else {
                self.$el.show();
            }
            _.each(shortcuts, function(s) {
                self.trigger('display', s);
            });
        });
    },
    add: function (sc) {
        var self = this;
        rpc.query({
            model: 'res.users.shortcut',
            method: 'create',
            args: [sc],
        }).then(function(out){
            self.trigger('load');
        });
    },
    display: function(sc) {
        var self = this;
        this.$el.find('.oe_systray_shortcut_menu').append();
        var $sc = $(qweb.render('Systray.ShortcutMenu.Item', {'shortcut': sc}));
        $sc.appendTo(self.$el.find('.oe_systray_shortcut_menu'));
    },
    remove: function (action_id, active_id) {
        var self = this;
        var $shortcut = this.$el.find('.oe_systray_shortcut_menu li a[data-action-id=' + action_id + '][data-active-id=' + active_id + ']');
        var shortcut_id = $shortcut.data('shortcut-id');
        $shortcut.parent().remove();
        rpc.query({
            model: 'res.users.shortcut',
            method: 'unlink',
            args: [shortcut_id],
        }).done(function () {
            var shortcuts = self.$el.find('.oe_systray_shortcut_menu li a');
            if (!shortcuts.length) {
                self.$el.hide();
            }
        });
    },
    click: function($link) {
        var self = this,
            menu_id = $link.data('id'),
            action_id = $link.data('action-id'),
            active_id = $link.data('active-id');
        self.trigger('click', action_id, menu_id, active_id);
    },
    has: function(menu_id, action_id, active_id) {
        // return !!this.$el.find('a[data-action-id=' + action_id + '][data-id=' + menu_id + ']').length;
        return !!this.$el.find('a[data-action-id=' + action_id + '][data-active-id=' + active_id + ']').length;
    }
});
SystrayMenu.Items.push(ShortcutMenu);

WebClient.include({
    show_application: function() {
        var self = this;
        var shortcuts_menu = null;
        return this._super.apply(this, arguments).then(function(res){
            if (!self.menu) {
                return res;
            }
            _.forEach(self.menu.systray_menu.widgets, function (item) {
                if(item.$el && item.$el.hasClass('x_shortcut')) {
                    return shortcuts_menu = item;
                }
            });
            if (shortcuts_menu) {
                x_shortcuts = shortcuts_menu;
                shortcuts_menu.on('click', this, function(action_id, menu_id, active_id) {
                    self.menu.current_secondary_menu = menu_id;
                    var options = {
                        clear_breadcrumbs: true,
                        replace_breadcrumb: true,
                    };
                    if (active_id) {
                        options['additional_context'] = {};
                        options['additional_context']['active_id'] = active_id;
                    }
                    self.do_action(action_id, options);
                });

                shortcuts_menu.on('click_setting', this, function(action_id) {
                    self.do_action(action_id, {
                        on_close: function () {
                            shortcuts_menu.load().done(function () {
                                if (!Object.keys(self.action_manager.actions).length) {
                                    return;
                                }
                                var action = self.action_manager.actions[self.action_manager.controllers[self.action_manager.controllerStack[0]].actionID];
                                self.action_manager.shortcut_check(action);
                            });
                        }
                    });
                });
            }
            return res;
        });
    }
});

ActionManager.include({
    doAction: function (action, options) {
        var self = this;
        return this._super.apply(this, arguments).done(function(action) {
            self.shortcut_check_loop(action);
            return action;
        });
    },
    _onBreadcrumbClicked: function(ev) {
        this._super.apply(this, arguments);
        var action = this.actions[this.controllers[ev.data.controllerID].actionID];
        this.shortcut_check(action);
    },
    shortcut_check: function(action) {
        var self = this;
        var $shortcut_toggle = $('.oe_shortcut_toggle');
        $shortcut_toggle.addClass('o_hidden');

        // Child view managers
        if (action.target != "current") {
            $shortcut_toggle.removeClass('o_hidden');
        }

        if (!action.id || action.target != "current"
            || ['ir.actions.act_window', 'ir.actions.server'].indexOf(action.type) === -1) {
            return;
        }

        var shortcuts_menu = x_shortcuts;
        if (shortcuts_menu) {
            var menu_id = self.__parentedParent.menu.current_secondary_menu;
            var primary_menu_id = self.__parentedParent.menu.current_primary_menu;
            if (!menu_id && primary_menu_id) {
                _.forEach(self.__parentedParent.menu.menu_data.children, function (item) {
                    if (item.id === primary_menu_id) {
                        if (item.children.length) {
                            if (!item.children[0].children.length)
                                return menu_id = item.children[0].id;
                            else {
                                return menu_id = item.children[0].children[0].id;
                            }
                        }
                    }
                });
            }
            if (!menu_id) {
                return;
            }
            $shortcut_toggle.removeClass('o_hidden');
            var active_id = action.context.active_id || 0;
            if (x_transient_models.indexOf(action.context.active_model) !== -1) {
                active_id = 0;
            }
            $shortcut_toggle.toggleClass('oe_shortcut_remove', shortcuts_menu.has(menu_id, action.id, active_id));
            $shortcut_toggle.unbind("click").click(function() {
                if ($shortcut_toggle.hasClass("oe_shortcut_remove")) {
                    if (!confirm(_t("Remove this shortcut item?"))) {
                        return;
                    }
                    shortcuts_menu.trigger('remove', action.id, active_id);
                    $shortcut_toggle.toggleClass("oe_shortcut_remove");
                } else {
                    var name = prompt(_t('Shortcut name'), action.display_name || action.name);
                    if (name != '') {
                        shortcuts_menu.trigger('add', {
                            'user_id': session.uid,
                            'menu_id': menu_id,
                            'action_id': action.id,
                            'active_id': active_id,
                            'name': name
                        });
                        $shortcut_toggle.toggleClass("oe_shortcut_remove");
                    }
                }
            });
        }
    },
    shortcut_check_loop: function(action) {
        var self = this;
        if (!x_shortcuts) {
            setTimeout(function () {
                self.shortcut_check_loop(action)
            }, 100);
        }
        else {
            setTimeout(function () {
                self.shortcut_check(action)
            }, 50);
        }
    }
});

return ShortcutMenu;
});
