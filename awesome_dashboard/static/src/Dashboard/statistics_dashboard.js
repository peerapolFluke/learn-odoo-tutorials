/** @odoo-module **/
import {registry} from "@web/core/registry";
import {reactive} from "@odoo/owl";

const statisticsDashboard = {
    dependencies: ["rpc"],
    start(env, {rpc}) {
        const statistics = reactive({isReady: false})

        const loadData = async () => {
            const data = await rpc("/awesome_dashboard/statistics", {})
            Object.assign(statistics, data, {isReady: true})
        }

        setInterval(loadData, 10 * 60 * 1000)
        loadData()
        return statistics
    }
}

registry.category("services").add("awesome_dashboard.statistics", statisticsDashboard)