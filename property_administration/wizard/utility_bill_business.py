# -*- coding: utf-8 -*-

from odoo import models, fields
import math


class TenancyBusinessUtilityBill(models.TransientModel):
    _name = "tenancy.business.utility.bill"
    _description = "Tenancy Business Utility Bill"

    date_start = fields.Date("Start Date")
    date_end = fields.Date("End Date")

    def create_utility_bill(self):
        tenancy_ids = self.env["property.tenancy"].browse(self.env.context.get("active_ids"))
        for rec in tenancy_ids:
            final_dict = {}
            postings = (
                self.env["businessplan.journal"]
                .search([("tenancy_id", "=", rec.id)])
                .filtered(
                    lambda x: not (
                        x.date_start < self.date_start and x.date_end < self.date_start
                    )
                )
                .filtered(
                    lambda x: not (
                        x.date_start > self.date_end and x.date_end > self.date_end
                    )
                )
            )
            data = {}
            new_posting_amount = 0
            for posting in postings:
                if posting.date_start <= self.date_start:
                    new_posting_amount += posting.amount
                    new_posting_vals = {
                        "date_start": self.date_start,
                        "date_end": self.date_end,
                        "amount": new_posting_amount,
                    }
                    data["date_start"] = new_posting_vals["date_start"]
                    data["date_end"] = new_posting_vals["date_end"]
                    data["amount"] = new_posting_vals["amount"]

                if posting.date_end >= self.date_end:
                    new_posting_amount += posting.amount
                    new_posting_vals = {
                        "date_start": self.date_start,
                        "date_end": self.date_end,
                        "amount": new_posting_amount,
                    }
                    data["date_start"] = new_posting_vals["date_start"]
                    data["date_end"] = new_posting_vals["date_end"]
                    data["amount"] = new_posting_vals["amount"]
                if posting.cost_type_id not in final_dict.keys():
                    final_dict[posting.cost_type_id] = [posting]
                else:
                    final_dict[posting.cost_type_id].append(posting)

            if final_dict:
                for d in final_dict:
                    # d = cost type
                    self.env["businessplan.businessplan"].create(
                        {
                            "expenditure_id": posting.expenditure_id.id,
                            "tenancy_id": rec.id,
                            "cost_type_id": d.id,
                            "amount": math.ceil(data["amount"]),
                            "date_start": data["date_start"],
                            "date_end": data["date_end"],
                        }
                    )
