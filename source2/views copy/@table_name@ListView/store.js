import { makeAutoObservable } from "mobx"
import { userApiClient } from 'src/components/ApiHelper'
import i18n from "i18next"
import MainStore from 'src/MainStore'

class NewStore {
    data = []
    openPanel = false
    currentId = 0

    fastInput = {
        idMain: 0,
        isEdit: false
    }


    constructor() {
        makeAutoObservable(this)
    }


    setFastInputIdMain = (id) => {
        this.fastInput.idMain = id
    }

    setFastInputIsEdit = (value) => {
        this.fastInput.isEdit = value
    }

    setCurrentId = (id) => {
        this.currentId = id
    }


    onButtonAddEditClick(id) {
        this.openPanel = true
        this.currentId = id
    }
    closePanel() {
        this.openPanel = false
        this.currentId = 0
    }

    @|template_store_index_load_function|@
        userApiClient(url)
            .then(json => {
                this.data = json
            })
            .catch(err => {
                MainStore.openErrorDialog(err.message)
            });
    }

    delete = (id, callback) => {
        userApiClient('/@|table_name|@/Delete', {
            method: "POST",
            body: id,
            headers: { "Content-type": "application/json; charset=UTF-8" }
        })
            .then(res => {
                MainStore.setSnackbar(i18n.t('message:snackbar.successSave'), 'success')
                callback(res)
            })
            .catch(ex => {
                MainStore.setSnackbar(i18n.t('message:snackbar.errorSave'), 'error')
                MainStore.openErrorDialog(ex.message)
            });

    }
}

export default new NewStore()
