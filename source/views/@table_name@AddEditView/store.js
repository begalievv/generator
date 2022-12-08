import { makeAutoObservable } from "mobx"
import { userApiClient } from 'src/components/ApiHelper'
import { validate } from './valid';
import i18n from 'i18next';
import { Save } from './save'
import MainStore from 'src/MainStore'

class NewStore {
    @|template_store_init|@

    // справочники лукапы
    @|template_store_init_dictionaries|@

    constructor() {
        makeAutoObservable(this)
    }

    clearStore() {
        @|template_store_clear|@
    }

    handleChange(event) {
        this[event.target.name] = event.target.value
        validate(event, (errorField, errorText) => { this[errorField] = errorText })
    }

    StoresSave(a, b, c) {
        Save(a, b, c)
    }

    onSaveClick = (props) => {

        const validated = (errorField, errorText) => { this[errorField] = errorText }

        var canSave = true
        @|template_store_validate|@

        if (canSave) {
            this.StoresSave(this, props, MainStore.openErrorDialog)
        }
        else {
            MainStore.openErrorDialog(i18n.t('message:error.alertMessageAlert'))
        }
    }

    @|template_store_load_dictionaries|@
    

    setData = (json) => {
        @|template_store_set_data|@
    }

    async doLoad(id) {

        this.clearStore()

        //загрузка справочников
        @|template_store_doload_dict|@

        var itemId = id != null || id != 0 ? id : this.id;

        if (itemId == null || itemId == 0) {
            return;
        }

        var url = '/@|table_name|@/GetOneById?id=' + itemId;
        userApiClient(url)
            .then(json => {
                this.setData(json)
            })
            .catch(err => {
                MainStore.openErrorDialog(err.message)
            });
    }
}

export default new NewStore()
