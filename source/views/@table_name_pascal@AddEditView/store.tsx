import { makeObservable, runInAction, observable } from "mobx";
import i18n from "i18next";
import dayjs, { Dayjs } from "dayjs";

import MainStore from "MainStore";
import BaseStore from 'core/stores/BaseStore';
import { validate, validateField } from "./valid";
import { get@|table_name_pascal|@, create@|table_name_pascal|@, update@|table_name_pascal|@ } from "api/@|table_name_pascal|@";
import { @|table_name_pascal|@, @|table_name_pascal|@CreateModel } from "constants/@|table_name_pascal|@";
@|template_store_import_dictionaries|@

interface @|table_name_pascal|@Response {
  id: number;
}

class @|table_name_pascal|@Store extends BaseStore {
  @|template_store_init|@

  // Справочники
  @|template_store_init_dictionaries|@


  constructor() {
    super();
    makeObservable(this);
  }

  clearStore() {
    super.clearStore();
    runInAction(() => {
      @|template_store_clear|@
    });
  }

  async validateField(name: string, value: any) {
    const { isValid, error } = await validateField(name, value);
    if (isValid) {
      this.errors[name] = ""; 
    } else {
      this.errors[name] = error;
    }
  }

  async onSaveClick(onSaved: (id: number) => void) {
    const data: @|table_name_pascal|@CreateModel = {
      @|template_store_validate|@
    };

    const { isValid, errors } = await validate(data);
    if (!isValid) {
      this.errors = errors;
      MainStore.openErrorDialog(i18n.t("message:error.alertMessageAlert"));
      return;
    }

    // Determine whether to create or update
    const apiMethod = data.id === 0 ?
      () => create@|table_name_pascal|@(data) :
      () => update@|table_name_pascal|@(data);

    // Make API call with inherited method
    this.apiCall(
      apiMethod,
      (response: @|table_name_pascal|@Response) => {
        if (data.id === 0) {
          runInAction(() => {
            this.id = response.id;
          });
          this.showSuccessSnackbar(i18n.t("message:snackbar.successSave"));
        } else {
          this.showSuccessSnackbar(i18n.t("message:snackbar.successEdit"));
        }
        onSaved(response.id || this.id);
      }
    );
  };

  async doLoad(id: number) {

    //загрузка справочников
    @|template_store_doload_dict|@

    if (id) {
      this.id = id;
      await this.load@|table_name_pascal|@(id);
    }
  }

  load@|table_name_pascal|@ = async (id: number) => {
    this.apiCall(
      () => get@|table_name_pascal|@(id),
      (data: @|table_name_pascal|@) => {
        runInAction(() => {
          @|template_store_set_data|@
        });
      }
    );
  };

  @|template_store_load_dictionaries|@

}

export default new @|table_name_pascal|@Store();
