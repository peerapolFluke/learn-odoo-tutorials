/** @odoo-module **/

import {Component, useState} from "@odoo/owl";
import {registry} from "@web/core/registry";
import {Layout} from "@web/search/layout";
import {useService} from "@web/core/utils/hooks";
import {_t} from "@web/core/l10n/translation";
import {DashboardItem} from "./components/DashboardItem/dashboard_item";
import {Dialog} from "@web/core/dialog/dialog";
import {CheckBox} from "@web/core/checkbox/checkbox";
import {browser} from "@web/core/browser/browser";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = {Layout, DashboardItem}

    setup() {
        this.display = {controlPanel: {}}
        this.action = useService("action")
        this.rpc = useService("rpc")
        this.dialog = useService("dialog")
        // @ts-ignore
        this.statistic = useState(useService("awesome_dashboard.statistics"))
        this.items = registry.category("awesome_dashboard").getAll()
        this.state = useState({
            disableItems: browser.localStorage.getItem('disableItem')?.split(',') || []
        })
    }

    openCustomer() {
        this.action.doAction("base.action_partner_form")
    }

    openLead() {
        this.action.doAction(
            {
                type: 'ir.actions.act_window',
                name: _t('All Leads'),
                res_model: 'crm.lead',
                views: [[false, 'list'], [false, 'form']],
            }
        )
    }

    onSaveConfiguration(newDisableItem) {
        this.state.disableItems = newDisableItem
    }

    openSetting() {
        this.dialog.add(ConfigurationDialog, {
            items: this.items,
            disableItems: this.state.disableItems,
            onSaveConfiguration: this.onSaveConfiguration.bind(this)
        })
    }
}

export class ConfigurationDialog extends Component {
    static template = "awesome_dashboard.ConfigurationDialog"
    static components = {Dialog, CheckBox}
    static props = ["close", "items", "disableItems", "onSaveConfiguration"]

    setup() {
        console.log('=.. SETUP')

        this.items = useState(this.props.items.map((item) => {
            return {
                ...item,
                enabled: !this.props.disableItems.some((disItem) => disItem === item.id)
            }
        }))
    }

    onChange(checked, changedItem) {
        const clone = [...this.items]
        clone[clone.findIndex((item) => item.id === changedItem.id)].enabled = checked
        this.items = clone
    }

    onClickDone() {
        const disableItem = Object.values(this.items.filter(
            (item) => !item.enabled
        ).map((item) => item.id))

        browser.localStorage.setItem(
            "disableItem",
            // @ts-ignore
            disableItem,
        )
        this.props.onSaveConfiguration(disableItem)
        this.props.close()
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
