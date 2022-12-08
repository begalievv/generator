import { makeAutoObservable } from "mobx"
import { userApiClient } from 'src/components/ApiHelper'
import { validate } from './valid';
import i18n from 'i18next';
import { Save } from './save'
import MainStore from 'src/MainStore'

class NewStore {
    
			id= 0
			name= ''
			description= ''
			code= ''
			queueNumber= ''
		errorname= ''
		errordescription= ''
		errorcode= ''
		errorqueueNumber= ''


    // справочники лукапы



    constructor() {
        makeAutoObservable(this)
    }

    clearStore() {
	this.id = 0	
		this.name = ''
		this.description = ''
		this.code = ''
		this.queueNumber = ''
		this.errorname= ''
		this.errordescription= ''
		this.errorcode= ''
		this.errorqueueNumber= ''

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
      var event = { target: { name: 'id', value: this.id, } };
      canSave = validate(event, validated) && canSave;
      var event = { target: { name: 'name', value: this.name, } };
      canSave = validate(event, validated) && canSave;
      var event = { target: { name: 'description', value: this.description, } };
      canSave = validate(event, validated) && canSave;
      var event = { target: { name: 'code', value: this.code, } };
      canSave = validate(event, validated) && canSave;
      var event = { target: { name: 'queueNumber', value: this.queueNumber, } };
      canSave = validate(event, validated) && canSave;


        if (canSave) {
            this.StoresSave(this, props, MainStore.openErrorDialog)
        }
        else {
            MainStore.openErrorDialog(i18n.t('message:error.alertMessageAlert'))
        }
    }


    // загрузка справочников
    // завершение справочников

    setData = (json) => {
		this.id= json.id	
		this.name= json.name	
		this.description= json.description	
		this.code= json.code	
		this.queueNumber= json.queueNumber

    }

    async doLoad(id) {

        this.clearStore()

        //загрузка справочников

        //загрузка справочников

        var itemId = id != null || id != 0 ? id : this.id;

        if (itemId == null || itemId == 0) {
            return;
        }

        var url = '/Valute/GetOneById?id=' + itemId;
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
