using App.General;
using DAL.EF.Context;
using DAL.Base;
using App;
using DAL.EF.Entities;
using System.Linq.Expressions;
using System;
using System.Linq;
using Microsoft.EntityFrameworkCore;
using System.Collections.Generic;

namespace DAL.General
{
    public class @|table_name|@Repository : BaseEfCrudRepository<@|table_name|@Dto, int, @|table_name|@>, I@|table_name|@Repository
    {
        public ISystemSettingProvider SystemSettingProvider { get; }
        public @|table_name|@Repository(ApplicationContext context, ISystemSettingProvider systemSettingProvider)
            : base(context)
        {
            SystemSettingProvider = systemSettingProvider;
        }

        protected override Func<@|table_name|@Dto, @|table_name|@> entitySelector => (@|table_name|@Dto x) => x.To@|table_name|@();
        protected override Expression<Func<@|table_name|@Dto, @|table_name|@>> entitySelectorExpr => (@|table_name|@Dto x) => x.To@|table_name|@();
        protected override Func<@|table_name|@, @|table_name|@Dto> dtoSelector => (@|table_name|@ x) => x.To@|table_name|@Dto();
        protected override Expression<Func<@|table_name|@, @|table_name|@Dto>> dtoSelectorExpr => (@|table_name|@ x) => x.To@|table_name|@Dto();
        protected override Expression<Func<@|table_name|@, bool>> filterSameItemsExpr(@|table_name|@Dto dto)
        {
            return x => false;
        }

        protected override IQueryable<@|table_name|@> TheWholeEntities => context.@|table_name_plural|@
            .AsNoTracking()
            @|template_repository_include|@
        ;

        @|template_repository|@
    }
}
