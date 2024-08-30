import { FC, useEffect } from 'react';
import {
  Container,
} from '@mui/material';
import PageGrid from 'components/PageGrid';
import { observer } from "mobx-react"
import store from "./store"
import { useTranslation } from 'react-i18next';
import { GridColDef } from '@mui/x-data-grid';
import PopupGrid from 'components/PopupGrid';
import @|table_name|@PopupForm from './../@|table_name|@AddEditView/popupForm'
import styled from 'styled-components';


type @|table_name|@ListViewProps = {
};


const @|table_name|@ListView: FC<@|table_name|@ListViewProps> = observer((props) => {
  const { t } = useTranslation();
  const translate = t;

  @|template_index_load_function|@


  const columns: GridColDef[] = [
    @|template_index_columns|@
  ];

  let type1: string = 'form';
  let component = null;
  switch (type1) {
    case 'form':
      component = <PageGrid
        title={translate("label:@|table_name|@ListView.entityTitle")}
        onDeleteClicked={(id: number) => store.delete@|table_name|@(id)}
        columns={columns}
        data={store.data}
        tableName="@|table_name|@" />
      break
    case 'popup':
      component = <PopupGrid
        title={translate("label:@|table_name|@ListView.entityTitle")}
        onDeleteClicked={(id: number) => store.delete@|table_name|@(id)}
        onEditClicked={(id: number) => store.onEditClicked(id)}
        columns={columns}
        data={store.data}
        tableName="@|table_name|@" />
      break
  }


  return (
    <Container maxWidth='xl' sx={{ mt: 4 }}>
      {component}

      <@|table_name|@PopupForm
        openPanel={store.openPanel}
        id={store.currentId}
        onBtnCancelClick={() => store.closePanel()}
        onSaveClick={() => {
          store.closePanel()
          store.load@|table_name_plural|@()
        }}
      />

    </Container>
  );
})



export default @|table_name|@ListView
