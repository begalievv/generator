using Core.Abstraction;
using App.Base;
using System;
using System.Collections.Generic;
using System.Globalization;

namespace App.General
{
    public class ContactTypeDto : IDtoWithId<int>
    {
        public int id { get; set; }
public string name { get; set; }
public string description { get; set; }
public string code { get; set; }

    }
}