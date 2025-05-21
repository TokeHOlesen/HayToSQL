class Report:
    """An essentially static class with methods that return different parts of the report in HTML format."""
    @staticmethod
    def generate_html_head() -> str:
        """
        Returns the first part of the HTML file, including the <head> section and the CSS.
        Doesn't accept arguments and is the same for all reports.
        """
        return ("""
<!DOCTYPE html>
<html lang="dk">
<head>
    <meta charset="UTF-8">
    <link href="https://fonts.googleapis.com/css2?family=Fira+Sans:wght@400;500;700&display=swap" rel="stylesheet">
    <title>Palissade ugerapport</title>
    <style>
        body {
            font-family: 'Fira Sans', sans-serif;
            margin: 0;
            padding: 0;
            background-color: #EAEAEA;
            color: #030303;
        }
        .container {
            width: 80%;
            margin: 0 auto;
            background: #FFFFFF;
            padding: 20px;
            box-shadow: 0 0 30px rgba(0,0,0,0.1);
        }
        .header {
            background-color: #56A2EF;
            color: #FFFFFF;
            padding: 10px 20px;
            text-align: center;
            border-radius: 5px;
        }
        .week-summary {
            color: #030303;
            padding: 2px 20px;
            margin: 10px auto;
            border: 2px solid lightblue;
            border-radius: 5px;
        }
        .day {
            margin-top: 20px;
            border: 2px solid lightblue;
            border-radius: 5px;
            padding: 0px 20px;
            padding-bottom: 20px;
            text-align: left;
            margin-bottom: 20px;
            background-color: #FFFFFF;
        }
        .kid {
            background-color: #F9F9F9;
            padding: 5px 10px 20px 10px;
            margin-top: 10px;
            padding-left: 40px;
            line-height: 0.8;
            border-left: 3px solid lightblue;
            position: relative;
            display: none;
        }
        .day.show-kids .kid {
            display: block;
        }
        .summary {
            font-size: 1.05em;
        }
        .big-order-box {
            margin-bottom: 20px;
            margin-left: 42px;
            display: block;
            width: fit-content;
        }
        .small-order-box {
            margin-bottom: 20px;
            margin-left: 42px;
            white-space: pre-wrap;
            word-break: break-all;
            line-height: 1.2;
        }
        .all-order-box {
            margin-bottom: 20px;
            margin-left: 42px;
            white-space: pre-wrap;
            word-break: break-all;
            line-height: 1.2;
        }
        .blue-box {
            background-color: #E0F7FA;
            border-radius: 5px;
            padding: 10px 10px;
            margin: 2px;
            border: 1px solid #B2EBF2;
            display: inline-block;
        }
        .red-box {
            background-color: #FCE4EC;
            border-radius: 5px;
            padding: 10px 10px;
            margin: 2px;
            border: 1px solid #F8BBD0;
            display: inline-block;
        }
        .yellow-box {
            background-color: #FFF9C4;
            border-radius: 5px;
            padding: 10px 10px;
            margin: 2px;
            border: 1px solid #FFF59D;
            display: inline-block;
        }
        .green-box {
            background-color: #E8F5E9;
            border-radius: 5px;
            padding: 10px 10px;
            margin: 2px;
            border: 1px solid #C8E6C9;
            display: inline-block;
        }
        .purple-box {
            background-color: #B2DFDB;
            border-radius: 5px;
            padding: 10px 10px;
            margin: 2px;
            border: 1px solid #80CBC4;
            display: inline-block;
        }
        button {
            padding: 5px 10px;
            width: 160px;
            font-size: 1em;
            background-color: #E0E0E0;
            color: #333;
            border: 1px solid #B0B0B0;
            border-radius: 5px;
            cursor: pointer;
        }
        button:hover {
            background-color: #D0D0D0;
        }
        button:active {
            background-color: #BEBEBE;
            transform: translateY(2px);
        }
        .order_contents {
            padding: 32px 10px 0px 10px;
            font-size: 0.9em;
            padding-left: 80px;
            display: none;
        }
        .order_contents table {
            border-collapse: collapse;
            margin-bottom: 10px;
        }
        .order_contents td, th {
            padding: 8px 15px;
            vertical-align: top;
            font-size: 0.9em;
            color: #333;
            border: 1px solid #E0E0E0;
        }
        .order_contents tr:nth-child(even) {
            background-color: #F9F9F9;
        }
        .order_contents tr:nth-child(odd) {
            background-color: #EAEAEA;
        }
        .order_contents th {
            background-color: #D0D0D0;
            font-weight: bold;
            text-align: left;
        }
        .kid.show-order-contents .order_contents {
            display: block;
        }
    </style>
</head>
<body>
    <div class="container">
""")

    @staticmethod
    def generate_header(start_date, end_date) -> str:
        """Returns the report header to display the date range covered by the report."""
        return (f"""
        <div class="header">
            <h1>Ugerapport for perioden {start_date.strftime("%d-%m-%Y")} - {end_date.strftime("%d-%m-%Y")}</h1>
        </div>
        """)

    @staticmethod
    def generate_week_summary(normal_items_total,
                              normal_items_in_small_orders,
                              normal_items_in_big_orders,
                              dsv_items_total,
                              normal_furniture_total,
                              dsv_furniture_total,
                              normal_cushions_total,
                              dsv_cushions_total,
                              orders_total,
                              small_orders_total,
                              big_orders_total,
                              ldm_total,
                              dsv_ldm_total,
                              dsv_number_by_day,
                              dsv_ldm_by_day,
                              kids_total,
                              kids_with_pick_series,
                              hay_direct_kids_total,
                              potentially_delayed_orders_total) -> str:
        """Returns the week summary section, with general overview of the week's orders."""

        # Generates the weekly overview and summary for DSV orders
        if dsv_furniture_total > 0:
            day_names = ["Mandag", "Tirsdag", "Onsdag", "Torsdag", "Fredag", "Lørdag", "Søndag"]
            dsv_summary = """
            <p class="summary"><strong>DSV-møbler per dag:</strong>
                <ul>
            """
            for i in range(7):
                if dsv_number_by_day[i] > 0:
                    dsv_summary += f"""
                    <li>{day_names[i]}: {dsv_number_by_day[i]} stk, {dsv_ldm_by_day[i]:.1f} ldm.</li>
                    """
            dsv_summary += """
                </ul>
            </p>
            """
        else:
            dsv_summary = """
            <p class="summary"><strong>Ingen møbler til DSV.</strong></p>
            """

        return (f"""
        <div class="week-summary">
            <p class="summary"><strong>Varer i alt:</strong> {normal_items_total + dsv_items_total} stk (alm. ordrer: {normal_items_total} stk ({normal_items_in_big_orders} på store ordrer, {normal_items_in_small_orders} på små ordrer), DSV ordrer: {dsv_items_total} stk).</p>
            <p class="summary"><strong>Møbler i alt i alt:</strong> {normal_furniture_total + dsv_furniture_total} stk (alm. ordrer: {normal_furniture_total} stk, DSV ordrer: {dsv_furniture_total} stk).</p>
            <p class="summary"><strong>Hynder i alt:</strong> {normal_cushions_total + dsv_cushions_total} stk (alm. ordrer: {normal_cushions_total} stk, DSV ordrer: {dsv_cushions_total} stk).</p>
            <p class="summary"><strong>Ca. lademeter i alt:</strong> {(ldm_total + dsv_ldm_total):.2f} ldm (alm. ordrer: {ldm_total} ldm, DSV ordrer: {dsv_ldm_total} ldm).</p>
            {dsv_summary}
            <p class="summary"><strong>Almindelige ordrer i alt:</strong> {orders_total}.</p>
            <p class="summary"><strong>Konsoliderede ordregrupper i alt (almindelige ordrer):</strong> {kids_total} (store: {big_orders_total}, små: {small_orders_total}) - {kids_with_pick_series} er sat i pluk.</p>
            <p class="summary"><strong>Hay-Direct ordrer:</strong> {hay_direct_kids_total}.</p>
            <p class="summary"><strong>Ordrer, der skal rykkes til ugen før:</strong> {potentially_delayed_orders_total}.</p>
        </div>
        """)

    @staticmethod
    def generate_day_head(weekday,
                          date,
                          items_total,
                          items_in_small_orders_total,
                          items_in_big_orders_total,
                          ldm_total,
                          orders_total,
                          small_orders_total,
                          big_orders_total,
                          kids_total,
                          kids_in_pick_series,
                          dates,
                          destinations,
                          order_list,
                          hay_direct_kids,
                          big_kids,
                          small_orders_list) -> str:
        """Returns the first part of the day overview section, with general information about the day."""

        hay_direct_orders = "<p><strong>Hay-Direct ordrer:</strong></p>" if hay_direct_kids else ""
        for kid in hay_direct_kids:
            hay_direct_orders += f"""
            <p class="big-order-box"><strong>{kid.country} - {kid.custname} ({kid.number_of_items} stk, ca. {round(kid.ldm, 2)} ldm):</strong> {' + '.join(kid.ordernumbers)}</p>
         """

        big_orders = "<p><strong>Store ordrer:</strong></p>" if big_kids and not big_kids == hay_direct_kids else ""
        for kid in big_kids:
            if kid not in hay_direct_kids:
                big_orders += f"""
            <p class="big-order-box"><strong>{kid.country} - {kid.custname} ({kid.number_of_items} stk, ca. {round(kid.ldm, 2)} ldm):</strong> {'|'.join(kid.ordernumbers)}</p>
        """

        small_orders = "<p><strong>Små ordrer:</strong></p>" if small_orders_list else ""
        small_orders += f"""
            <p class="small-order-box">{'|'.join(small_orders_list)}</p>
        """

        if items_total > 0:
            return (f"""
        <div class="day">
            <h2>{weekday} d. {date.strftime("%d-%m-%Y")}</h2>
            <p><strong>Varer i alt:</strong> {items_total} (på store ordrer: {items_in_big_orders_total}, på små ordrer: {items_in_small_orders_total}).</p>
            <p><strong>Ca. ldm i alt:</strong> {round(ldm_total, 2)} ldm.</p>
            <p><strong>Ordrer i alt:</strong> {orders_total}.</p>
            <p><strong>Konsoliderede ordregrupper i alt:</strong> {kids_total} (store: {big_orders_total}, små: {small_orders_total}) - {kids_in_pick_series} er sat i pluk.</p>
            <p><strong>Ordrerne har følgende bekræftede leveringsdatoer:</strong> {', '.join([date.strftime("%d-%m-%Y") for date in dates])}.</p>
            <p><strong>Destinationer:</strong> {', '.join(destinations)}.</p>
            {hay_direct_orders}
            {big_orders}
            {small_orders}
            <p><strong>Alle ordrer:</strong></p>
            <p class="all-order-box">{'|'.join(order_list)}</p>
            <button onclick="toggleKids(this)">Vis KID'er</button>
        """)
        return (f"""
        <div class="day">
            <h2>{weekday} d. {date.strftime("%d-%m-%Y")}</h2>
            <p>Der er ingen ordrer til denne dag eller det hele er allerede blevet pakket.</p>
        """)

    @staticmethod
    def generate_kid(kid_number,
                     custname,
                     pick_series,
                     city,
                     country,
                     confirmed_dates,
                     orders_total,
                     items_total,
                     ldm_total,
                     order_numbers,
                     is_moved_back,
                     is_delayed,
                     is_hay_direct,
                     is_big,
                     all_items) -> str:
        """Returns code for displaying data of single Kid."""

        ordre_dato_msg, ordre_msg = ("Ordren", "ordre") if orders_total == 1 else ("Ordrerne", "ordrer")
        vare_msg = "vare" if items_total == 1 else "varer"

        tags = []
        if is_delayed:
            tags.append('<p class="red-box">Forsinkelsesrisiko: ordren skal rykkes til ugen før</p>')
        if is_hay_direct:
            tags.append('<p class="yellow-box">Hay-Direct ordre</p>')
        if is_moved_back and not is_delayed:
            tags.append('<p class="purple-box">Rykket frem for at matche leveringsdatoen for dette land</p>')
        if is_big:
            tags.append('<p class="blue-box">Stor ordre</p>')
        if pick_series:
            tags.append('<p class="green-box">Er sat i pluk</p>')
        all_tags = "\n                ".join(tags)

        order_contents_rows = ""
        for item in all_items:
            order_contents_rows += (f"""
                    <tr>
                        <td>{item.item_number}</td>
                        <td>{item.item_name}</td>
                        <td>{item.item_color}</td>
                        <td>{item.number}</td>
                    </tr>
            """)

        return (f"""
            <div class="kid">
                <h3>Konsolideret ordregruppe nr. {kid_number}:</h3>
                {all_tags}
                <p>{custname}, {city}, {country}.</p>
                {f"<p>Plukserie: {pick_series}</p>" if pick_series else ""}
                <p>{orders_total} {ordre_msg}, {items_total} {vare_msg}, ca. {round(ldm_total, 2)} ldm.</p>
                <p>{ordre_dato_msg} er bekræftet til d.: {', '.join([date.strftime("%d-%m-%Y") for date in confirmed_dates])}.</p>
                <p class="filter-values">{'|'.join(order_numbers)}</p>
                <button onclick="toggleOrderContents(this)">Vis varer</button>
                <div class="order_contents">
                    <table>
                        <tr>
                            <th style="width: 150px;">Varenummer</th>
                            <th style="width: 300px;">Navn</th>
                            <th style="width: 130px;">Farve</th>
                            <th style="width: 50px;">Antal</th>
                        </tr>
                        {order_contents_rows}
                    </table>
                </div>    
            </div>        
        """)

    @staticmethod
    def generate_day_tail() -> str:
        """Returns the closing tag for the Day section."""
        return ("""
        </div>
        """)

    @staticmethod
    def generate_html_tail() -> str:
        """Returns the final part of the file, including the JS and the closing tags."""
        return ("""
    </div>
    <script>
        // toggles visibility of individual KID elements
        function toggleKids(button) {
            const dayDiv = button.closest('.day');
            dayDiv.classList.toggle('show-kids');
            
            if (dayDiv.classList.contains('show-kids')) {
                button.textContent = "Skjul KID'er";
            } else {
                button.textContent = "Vis KID'er";
            }
        }
    </script>
    <script>
        // toggles visibility of items on this KID
        function toggleOrderContents(button) {
            const kidDiv = button.closest('.kid');
            kidDiv.classList.toggle('show-order-contents');
            
            if (kidDiv.classList.contains('show-order-contents')) {
                button.textContent = "Skjul varer";
            } else {
                button.textContent = "Vis varer";
            }
        }
    </script>
</body>
</html>
        """)
