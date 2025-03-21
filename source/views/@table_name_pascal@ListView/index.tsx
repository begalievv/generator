import React, { FC, useEffect } from 'react';
import { observer } from "mobx-react";
import dayjs from "dayjs";
import { useTranslation } from 'react-i18next';
import { GridColDef } from '@mui/x-data-grid';
import BaseListView from 'components/common/BaseListView';
import @|table_name_pascal|@PopupForm from '../@|table_name_pascal|@AddEditView/popupForm';
import store from "./store";


type @|table_name_pascal|@ListViewProps = {
  @|template_index_props_idmain|@
};


const @|table_name_pascal|@ListView: FC<@|table_name_pascal|@ListViewProps> = observer((props) => {
  const { t } = useTranslation();
  const translate = t;

  @|template_index_set_main|@

  const columns: GridColDef[] = [
    @|template_index_columns|@
  ];

  return (
    <BaseListView
      maxWidth={"xl"}
      title={translate("label:@|table_name_pascal|@ListView.entityTitle")}
      columns={columns}
      data={store.data}
      tableName="@|table_name_pascal|@"
      onDeleteClicked={(id) => store.delete@|table_name_pascal|@(id)}
      onEditClicked={(id) => store.onEditClicked(id)}
      store={{
        loadData: store.load@|table_name_pascal|@s,
        clearStore: store.clearStore
      }}
      viewMode="@|template_index_is_popup|@"
    >
      <@|table_name_pascal|@PopupForm
        openPanel={store.openPanel}
        id={store.currentId}
        onBtnCancelClick={() => store.closePanel()}
        onSaveClick={() => {
          store.closePanel();
          store.load@|table_name_pascal|@s();
        }}
      />
    </BaseListView>
  );
})



export default @|table_name_pascal|@ListView
