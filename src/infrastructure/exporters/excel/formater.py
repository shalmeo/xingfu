from openpyxl.styles import Alignment, Border, Side
from openpyxl.worksheet.worksheet import Worksheet


class Formatter:
    def __init__(self, worksheet: Worksheet):
        self.worksheet = worksheet

    def format_row(self, row: int, max_col=None) -> None:
        self.worksheet.row_dimensions[row].height = 30
        for row in self.worksheet.iter_cols(min_row=row, max_row=row, max_col=max_col):
            cell = next(iter(row))
            cell.alignment = Alignment(
                horizontal="center", vertical="center", wrap_text=True
            )

            if cell.column == 1:
                cell.border = Border(
                    left=Side(style="medium"),
                    top=Side(style="medium", color="CCCCCC"),
                    bottom=Side(style="medium", color="CCCCCC"),
                    right=Side(style="medium", color="CCCCCC"),
                )
            elif cell.column == max_col:
                cell.border = Border(
                    right=Side(style="medium"),
                    top=Side(style="medium", color="CCCCCC"),
                    bottom=Side(style="medium", color="CCCCCC"),
                    left=Side(style="medium", color="CCCCCC"),
                )
            else:
                cell.border = Border(
                    top=Side(style="medium", color="CCCCCC"),
                    bottom=Side(style="medium", color="CCCCCC"),
                    right=Side(style="medium", color="CCCCCC"),
                    left=Side(style="medium", color="CCCCCC"),
                )
