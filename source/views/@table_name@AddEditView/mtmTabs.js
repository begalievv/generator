import React from 'react';
import PropTypes from 'prop-types';
import SwipeableViews from 'react-swipeable-views';
import { withStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import Typography from '@material-ui/core/Typography';
@|template_mtm_import|@
import { Card, CardContent } from '@material-ui/core';
import { withTranslation } from 'react-i18next';
import store from "./store"
import { observer } from "mobx-react"


function TabPanel(props) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role='tabpanel'
      hidden={value !== index}
      id={`full-width-tabpanel-${index}`}
      aria-labelledby={`full-width-tab-${index}`}
      {...other}
    >
      <Typography>{children}</Typography>
    </div>
  );
}

TabPanel.propTypes = {
  children: PropTypes.node,
  index: PropTypes.any.isRequired,
  value: PropTypes.any.isRequired
};

function a11yProps(index) {
  return {
    id: `wrapped-tab-${index}`,
    'aria-controls': `wrapped-tabpanel-${index}`
  };
}

const useStyles = (theme) => ({
  root: {}
});


const FullWidthTabs = observer(
  class FullWidthTabs extends React.Component {
    constructor(props) {
      super(props);
      this.state = {
        value: 0,
        theme: undefined
      }
    }

    handleChange = (event, newValue) => {
      this.setState({ value: newValue });
    };

    handleChangeIndex = (index) => {
      this.setState({ value: index });
    };

    render() {
      const { t } = this.props
      const translate = t
      const { classes, theme } = this.props;
      console.log(store.id)
      return (
        <div className={classes.root}>
          <AppBar position='static' color='default'>
            <Tabs
              value={this.state.value}
              onChange={this.handleChange}
              variant='standard'
              aria-label='wrapped label tabs example'
            >

              @|template_mtm_title|@
            </Tabs>
          </AppBar>

          <SwipeableViews
            axis={theme.direction === 'rtl' ? 'x-reverse' : 'x'}
            index={this.state.value}
            onChangeIndex={this.handleChangeIndex}
          >
            
            @|template_mtm_content|@
          </SwipeableViews>
        </div>
      );
    }
  }
)

export default withTranslation(['label'])(withStyles(useStyles, { withTheme: true })(FullWidthTabs));
