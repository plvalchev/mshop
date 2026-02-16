#!/usr/bin/env python3
"""
Extract new product URLs that aren't already in products.json
"""
import json

# All URLs from pages 1-6
all_urls = [
    # Page 1 (36 URLs)
    "https://vendora.bg/items/n0m21yp/mini-parfyumi-neblina-i-dillys-novi-avtentichni.html",
    "https://vendora.bg/items/jpqwgok/mini-parfyum-sun-moon-stars-karl-lagerfeld-nov-35-ml.html",
    "https://vendora.bg/items/gx38xxd/mini-parfyumi-novi-komplekt-s-neblina-creature-cantate-dily.html",
    "https://vendora.bg/items/qqy53w1/be-bop-kesling-mini-parfyum-nov-toaletna-voda-75-ml.html",
    "https://vendora.bg/items/dyoe5mj/mini-parfyum-crature-by-gilles-cantuel-45-ml-nov-toaletna-voda.html",
    "https://vendora.bg/items/2oqkw09/romeo-di-romeo-gigli-mini-parfyum-nov-75-ml.html",
    "https://vendora.bg/items/114ezg8/red-jeans-versace-mini-parfyum-nov-75-ml-toaletna-voda.html",
    "https://vendora.bg/items/n0m5znp/cabochard-great-mini-parfyum-nov-18-ml.html",
    "https://vendora.bg/items/7y56p2j/magie-noir-lancome-mini-parfyum-nov-75-ml.html",
    "https://vendora.bg/items/114keyz/shafali-fleur-rare-yves-rocher-mini-parfyum-nov-75-ml.html",
    "https://vendora.bg/items/kyz3wm0/ispahan-yves-rocher-miniatyuren-parfyum-15-ml-nov.html",
    "https://vendora.bg/items/dyoj690/green-jeans-versace-mini-parfyum-nov-75-ml.html",
    "https://vendora.bg/items/qqy5qwz/invictus-paco-rabanne-mini-parfyum-nov-5-ml.html",
    "https://vendora.bg/items/xqgp3m8/mini-parfyum-silver-rain-la-prairie-2-ml-nov.html",
    "https://vendora.bg/items/dyoex0p/nocturnes-de-caron-mini-parfyum-nov-toaletna-voda-5-ml.html",
    "https://vendora.bg/items/ojy5gqw/michelle-balenciaga-mini-parfyum-nov-ryadk-kolekcionerski-ekzemplyar-5-ml.html",
    "https://vendora.bg/items/mmp7y68/knowing-este-lauder-mini-parfyum-nov-35-ml.html",
    "https://vendora.bg/items/4ep832m/drakkar-noir-guy-laroche-mini-parfyum-nov-5-ml-toaletna-voda.html",
    "https://vendora.bg/items/114ez28/blue-jeans-versace-mini-parfyum-nov-75-ml.html",
    "https://vendora.bg/items/zjqmw11/vent-vent-pierre-balmain-mini-parfyum-nov-toaletna-voda-4-ml.html",
    "https://vendora.bg/items/9xze501/vent-vent-pierre-balmain-mini-parfyum-nov-kolekcionerska-opakovka.html",
    "https://vendora.bg/items/xqgwmj7/mini-parfyum-regines-5-ml-nov.html",
    "https://vendora.bg/items/n0m50eg/autograph-intense-marks-spencer-toaletna-voda-za-mzhe-upotrebyavana-30-ml.html",
    "https://vendora.bg/items/xqgp5nd/ungaro-diva-mini-parfyum-nov-45-ml.html",
    "https://vendora.bg/items/p4yw07o/loulou-blue-cacharel-tester-parfyum-nov-18-ml.html",
    "https://vendora.bg/items/wm3pdwg/mini-parfyum-sun-moon-stars-karl-lagerfeld-nov-37-ml.html",
    "https://vendora.bg/items/kyzo9p1/signature-dupont-mini-parfyum-nov-kolekcionerski-5-ml.html",
    "https://vendora.bg/items/wm3p9dg/very-valentino-mini-parfyum-nov-kolekcionerski-45-ml.html",
    "https://vendora.bg/items/4ep8ywy/dkny-be-delicious-extra-mini-parfyum-nov-75-ml.html",
    "https://vendora.bg/items/9xze244/mini-parfyum-eau-de-givenchy-nov-4-ml-toaletna-voda.html",
    "https://vendora.bg/items/mmp71eg/signorina-libera-salvatore-ferragamo-mini-parfyum-nov-5-ml.html",
    "https://vendora.bg/items/jpq5yqk/one-essence-calvin-klein-intense-mini-parfyum-nov-10-ml.html",
    "https://vendora.bg/items/mmp7zng/sergio-tacchini-mini-parfyum-nov-8-ml-toaletna-voda.html",
    "https://vendora.bg/items/ojywoxy/mini-parfyum-les-belles-nina-ricci-nov-4-ml-toaletna-voda.html",
    "https://vendora.bg/items/jpq528j/jimmy-choo-fever-mini-parfyum-nov-45-ml.html",
    "https://vendora.bg/items/n0m3o43/leau-de-sonia-rykiel-mini-parfyum-nov-toaletna-voda-5-ml.html",

    # Page 2 (36 URLs)
    "https://vendora.bg/items/2oq5q65/daisy-love-glow-marc-jacobs-50ml-nov-limitirano-izdanie.html",
    "https://vendora.bg/items/xq60j98/van-gils-pour-homme-mini-parfyum-nov-toaletna-voda-10-ml.html",
    "https://vendora.bg/items/wm5z2ee/lalique-pour-homme-mini-parfyum-nov-5-ml.html",
    "https://vendora.bg/items/8e206yq/mini-parfyum-nature-yves-rocher-5ml-kato-novo.html",
    "https://vendora.bg/items/6kdx111/blue-ralph-lauren-mini-parfyum-nov-toaletna-voda-75-ml.html",
    "https://vendora.bg/items/4e2407y/mini-parfyum-trussardi-6ml-nov-avtentichen.html",
    "https://vendora.bg/items/n03o3qp/sapun-moschino-cheap-chic-25gr-nov.html",
    "https://vendora.bg/items/9xe8oj4/prada-paradox-intense-90ml-nov-eau-de-parfum-s-kutiya.html",
    "https://vendora.bg/items/jp5zj48/korres-cashmere-kumquat-eau-de-toilette-damski-parfyum-10-ml-nov-s-kutiya.html",
    "https://vendora.bg/items/wmp1x6g/signorina-ribelle-ferragamo-eau-de-parfum-100-ml-nov-s-kutiya.html",
    "https://vendora.bg/items/3no3q45/burberry-her-mini-komplekt-novi-parfyumni-miniatyuri-5ml.html",
    "https://vendora.bg/items/7ygdxzj/paco-rabanne-invictus-mini-parfyum-5-ml-nov-ryadk-kolekcionerski.html",
    "https://vendora.bg/items/7yg80wj/leau-jolie-mini-parfyum-5-ml-ot-lolita-lempicka-v-kolekcionerska-opakovka.html",
    "https://vendora.bg/items/zj88m10/jean-paul-gaultier-le-beau-mini-parfyum-nov-7ml-eau-de-parfum.html",
    "https://vendora.bg/items/0ydd10e/divine-eau-de-parfum-na-jean-paul-gaultier-miniatyuren-parfyum-nov-avtentichen.html",
    "https://vendora.bg/items/qj72mp/display-case-kato-nov-s-14-otdeleniya-pleksiglas-i-akrilno-ogledalo.html",
    "https://vendora.bg/items/p087nd/eternity-moment-by-calvin-klein-15ml-nov.html",
    "https://vendora.bg/items/mq115k/lipgloss-handaiyan-komplekt-techen-mat-6-x-25-ml-nov.html",
    "https://vendora.bg/items/ymj6z7/boucheron-initial-body-cream-kato-nov-30-ml.html",
    "https://vendora.bg/items/mq1eoo/lalique-satin-eau-de-parfume-15ml-nov.html",
    "https://vendora.bg/items/o2o3d0/kozmetichna-chanta-armani-si-rozova-nova.html",
    "https://vendora.bg/items/2j3ngq/quantum-pendant-nov-dlzhina-80sm.html",
    "https://vendora.bg/items/107m0p/chlo-eau-de-parfume-roll-on-6ml-upotrebyavan.html",
    "https://vendora.bg/items/x50xkd/wonderful-neckless-novo-dlzhina-na-verizhkata-50sm.html",
    "https://vendora.bg/items/p087o5/perry-for-her-miniatyuren-parfyum-75-ml-nov.html",
    "https://vendora.bg/items/56q33w/hermes-jardin-komplekt-ot-4-mini-parfyuma-75-ml-novi.html",
    "https://vendora.bg/items/618wom/milestone-club-de-nuit-30ml-armaf-nov.html",
    "https://vendora.bg/items/2jn2jy/komplekt-gucci-flora-4-x-5-ml-miniatyurni-parfyumi-novi.html",
    "https://vendora.bg/items/dm7wd1/intense-woman-club-de-nuit-30ml-armaf-novo.html",
    "https://vendora.bg/items/4z1n2k/woman-club-de-nuit-30ml-armaf-nov.html",
    "https://vendora.bg/items/nxn6mp/ghost-the-fragrance-100ml-nov.html",
    "https://vendora.bg/items/7p7n98/opium-miniature-perfume-yves-saint-laurent-nov-75-ml.html",
    "https://vendora.bg/items/2j3pk3/kolekcionerska-kutiya-channel-no-5-nova.html",
    "https://vendora.bg/items/4z19ky/alessandro-dell-acqua-miniatyuren-parfyum-nov-4-ml.html",
    "https://vendora.bg/items/o26eqo/escada-acte-2-mini-parfyum-nov-plen-4-ml-eau-de-parfum.html",
    "https://vendora.bg/items/j3253x/miniatyuren-parfyum-givenchy-iii-givenchy-kato-nov-4ml.html",

    # Page 3 (36 URLs)
    "https://vendora.bg/items/go4m92/mini-parfyum-knowing-estee-lauder-nov-35-ml.html",
    "https://vendora.bg/items/ym20ww/givenchy-iii-givenchy-miniatyuren-parfyum-4-ml-kato-nov.html",
    "https://vendora.bg/items/02jejk/chopard-cashmere-miniatyuren-parfyum-kato-nov-5-ml.html",
    "https://vendora.bg/items/p076zd/amarige-givenchy-miniatyuren-parfyum-nov-4-ml.html",
    "https://vendora.bg/items/7pzqd8/parfyum-ombre-rose-jean-charles-brosseau-5ml-nov.html",
    "https://vendora.bg/items/61m6o6/nocturnes-de-caron-mini-parfyum-nov-plen-5ml.html",
    "https://vendora.bg/items/61mzk1/lancme-trsor-parfyum-miniatyura-nov-75-ml.html",
    "https://vendora.bg/items/615ykq/mini-parfyum-trussardi-6ml-nov-plen.html",
    "https://vendora.bg/items/4z69my/parfyum-coco-channel-miniature-eau-de-toilet-4ml-nov.html",
    "https://vendora.bg/items/7p9ee3/miniatyuren-parfyum-samba-75-ml-nov.html",
    "https://vendora.bg/items/10w3e6/happy-clinique-miniatyuren-parfyum-4ml-nov.html",
    "https://vendora.bg/items/ym46do/chloe-karl-lagerfeld-miniatyuren-parfyum-37-ml-nov.html",
    "https://vendora.bg/items/2jqp3g/xeryous-by-givenchy-miniatyuren-parfyum-kato-nov-4-ml.html",
    "https://vendora.bg/items/8w18dw/chloe-narcisse-miniatyuren-parfyum-nov-37-ml.html",
    "https://vendora.bg/items/go3q42/mini-parfyum-regines-by-regines-5-ml-nov.html",
    "https://vendora.bg/items/104p7d/mini-parfyum-eau-belle-by-azzaro-4-ml-nov.html",
    "https://vendora.bg/items/j35kwj/givenchy-ysatis-miniatyuren-parfyum-nov-4ml-eau-de-parfum.html",
    "https://vendora.bg/items/o2w260/hot-couture-givenchy-miniatyuren-parfyum-nov-5-ml.html",
    "https://vendora.bg/items/02036w/oh-la-la-by-azzaro-miniatyuren-parfyum-3ml-nov-vintidzh.html",
    "https://vendora.bg/items/3yoqpd/calvin-klein-truth-mini-parfyum-nov-4-ml-vintidzh-plen.html",
    "https://vendora.bg/items/kgop79/4711-eau-de-cologne-miniatyura-kato-nova-3-ml.html",
    "https://vendora.bg/items/8wzp0q/parfyum-solo-rosa-miniature-luciano-soprani-nov.html",
    "https://vendora.bg/items/kgo28k/popy-moreni-miniatyuren-parfyum-nov-vintidzh-ot-90-te.html",
    "https://vendora.bg/items/mq7oe8/montana-suggestion-miniatyuren-parfyum-nov-3-ml-vintidzh.html",
    "https://vendora.bg/items/8wzp2w/maroussia-slava-zatsev-mini-parfyum-kato-nov.html",
    "https://vendora.bg/items/j39qqn/miss-dior-cherries-mini-parfyum-nov-5-ml.html",
    "https://vendora.bg/items/1058o8/dolce-gabbana-light-blue-mini-parfyum-nov-45-ml-eau-de-toilette.html",
    "https://vendora.bg/items/o2kz1y/organza-givency-miniatyuren-parfyum-5-ml-nov-vintidzh.html",
    "https://vendora.bg/items/2j1q3g/salvador-dali-eau-de-toilette-mini-parfyum-nov-8-ml.html",
    "https://vendora.bg/items/ymo4zw/dolce-gabbana-di-dolce-e-gabbana-miniatyuren-eau-de-toilette-5ml-nov.html",
    "https://vendora.bg/items/56d05k/fahrenheit-by-cristian-dior-miniatyuren-parfyum-10-ml-kato-nov.html",
    "https://vendora.bg/items/ek2nxg/dolce-vita-christian-dior-miniatyuren-parfyum-5ml-nov.html",
    "https://vendora.bg/items/dmn5qj/rochas-man-miniatyuren-parfyum-kato-nov-5ml.html",
    "https://vendora.bg/items/zk8qxz/parfyum-tribu-united-colors-of-benetton-upotrebyavan-4-ml-napukan-kapak.html",
    "https://vendora.bg/items/95d3m6/dalimix-salvador-dali-miniatyuren-parfyum-8ml-nov.html",
    "https://vendora.bg/items/ymow37/my-burberry-miniatyuren-parfyum-nov-5ml.html",

    # Page 4 (36 URLs)
    "https://vendora.bg/items/x57p8d/oh-de-moschino-miniatyuren-parfyum-kato-nov-4-ml-zhena.html",
    "https://vendora.bg/items/ymok8d/rochas-fleur-d-eau-eau-de-toilette-za-zheni-5-ml-nov.html",
    "https://vendora.bg/items/8wk41m/versace-dylan-blue-pour-homme-miniatyuren-parfyum-nov-5ml.html",
    "https://vendora.bg/items/02dw1k/parfyum-sonia-rykiel-miniature-75-ml-nov-edt-za-zheni.html",
    "https://vendora.bg/items/j39j2j/moschino-toy-2-bubble-gum-mini-parfyum-nov-5-ml.html",
    "https://vendora.bg/items/o2kw94/cheap-and-chic-by-moschino-miniatyuren-parfyum-kato-nov-vintidzh-1990-te-49-ml.html",
    "https://vendora.bg/items/qj8w61/lalique-le-parfume-miniatyuren-parfyum-kato-nov-45-ml.html",
    "https://vendora.bg/items/x5776x/paradox-jacomo-parfyum-miniatyura-5-ml-nov.html",
    "https://vendora.bg/items/02donw/lauren-by-ralph-lauren-miniatyuren-parfyum-35-ml-nov.html",
    "https://vendora.bg/items/kgkom9/mini-parfyum-neblina-by-yves-rocher-75-ml-nov.html",
    "https://vendora.bg/items/61jgj1/jean-paul-gautier-le-male-miniatyuren-parfyum-nov-35-ml.html",
    "https://vendora.bg/items/ym3mnd/ricci-ricci-ot-nina-ricci-miniatyuren-parfyum-nov-4ml.html",
    "https://vendora.bg/items/ek22gg/miniatyuren-parfyum-fendi-edt-vintidzh-1990-te-5-ml-nov-plen.html",
    "https://vendora.bg/items/10dqw8/le-roy-soleil-by-salvador-dali-miniatyuren-parfyum-5ml-nov.html",
    "https://vendora.bg/items/o2kj34/fiorucci-eau-de-toilette-miniatyura-kato-nov-5ml.html",
    "https://vendora.bg/items/x52536/jadore-by-christian-dior-5ml-nov.html",
    "https://vendora.bg/items/8w9d8p/lalique-honeysuckle-mini-parfyum-nov-45-ml.html",
    "https://vendora.bg/items/j3j328/leau-cheap-and-chic-moschino-edt-nov-miniatyuren-parfyum-49-ml.html",
    "https://vendora.bg/items/7pxm53/chopard-camir-parfyum-miniatyura-nov-5ml-eau-de-parfum.html",
    "https://vendora.bg/items/nxk85q/oscar-by-orcar-de-la-renta-miniatyuren-parfyum-nov-4ml-vintidzh-plen.html",
    "https://vendora.bg/items/7pxpy9/vintage-nino-cerruti-pour-femme-eau-de-parfum-miniatyura-nova-37-ml.html",
    "https://vendora.bg/items/7pxpdj/donna-trussardi-vintage-eau-toilette-mini-parfyum-kato-nov-5ml.html",
    "https://vendora.bg/items/8w9wqm/blumarine-parfyum-miniatyura-5ml-nov.html",
    "https://vendora.bg/items/x5mn08/prada-la-femme-miniature-9ml-novo.html",
    "https://vendora.bg/items/7p47y3/iceberg-twice-ice-parfyum-miniatyura-kato-nov-45-ml-za-mzhe.html",
    "https://vendora.bg/items/07g4mw/nuxe-multi-purpose-dry-oil-nov-10-ml.html",
    "https://vendora.bg/items/13q098/lancome-tresor-miniatyuren-vintidzh-parfyum-5ml-nov.html",
    "https://vendora.bg/items/13z8yz/carolina-herrera-red-pouch-novo.html",
    "https://vendora.bg/items/13z538/miniatyuren-eau-de-toilette-h24-herms-nov-5-ml.html",
    "https://vendora.bg/items/70pmy8/eros-versace-mini-parfyum-nov-5-ml.html",
    "https://vendora.bg/items/9y59m6/guy-laroche-drakkar-noir-mini-parfyum-5ml-nov.html",
    "https://vendora.bg/items/8jwy8w/sicily-by-dolce-and-gabbana-miniatyuren-parfyum-kato-nov-4-ml.html",
    "https://vendora.bg/items/ngx62g/lancme-miracle-parfyum-miniatyura-nov-5-ml.html",
    "https://vendora.bg/items/4q07gm/moschino-glamour-miniatyuren-parfyum-nov-5-ml.html",
    "https://vendora.bg/items/2gjg35/joop-night-flight-mini-parfyum-nov-5-ml.html",
    "https://vendora.bg/items/0723gk/invictus-paco-rabanne-mini-parfyum-nov-5-ml.html",

    # Page 5 (36 URLs)
    "https://vendora.bg/items/zwkw30/skin-trussardi-miniatyuren-parfyum-5-ml-nov.html",
    "https://vendora.bg/items/pq05wd/miniatyura-parfyum-linsolent-charles-jourdan-nova-plna-375-ml.html",
    "https://vendora.bg/items/epk70k/daisy-by-marc-jacobs-miniatyuren-parfyum-upotrebyavan-4-ml.html",
    "https://vendora.bg/items/k8g8q5/a-scent-by-issey-miyake-miniatyuren-parfyum-nov-75-ml.html",
    "https://vendora.bg/items/jo3dgk/versace-yellow-diamond-miniatyuren-parfyum-nov-5-ml.html",
    "https://vendora.bg/items/m3qy1g/clo-eau-de-perfume-miniature-5-ml-nov.html",
    "https://vendora.bg/items/70pj69/michael-kors-pour-femme-mini-parfyum-nov-5-ml-eau-de-perfume.html",
    "https://vendora.bg/items/34yqe0/parfyum-gieffeffe-by-ferre-miniature-kato-nov.html",
    "https://vendora.bg/items/9y51wn/cachet-damski-parfyum-nov-15-ml-ot-prince-matchabelli.html",
    "https://vendora.bg/items/d1m2z0/anais-anais-cacharel-parfyum-upotrebyavan-5ml-plen.html",
    "https://vendora.bg/items/qxjd2g/miniatyuren-parfyum-versense-versace-5-ml-nov.html",
    "https://vendora.bg/items/8jw0xq/parfyum-rochas-byzance-miniatyura-3ml-nov.html",
    "https://vendora.bg/items/qxj9ng/alchimie-rochas-miniatyuren-parfyum-5ml-vintidzh-1989-nov.html",
    "https://vendora.bg/items/w6w7dz/nina-ricci-fleur-de-fleurs-miniatyuren-parfyum-6ml.html",
    "https://vendora.bg/items/2gj8qg/vanitas-versace-miniatyuren-parfyum-nov-4-ml.html",
    "https://vendora.bg/items/4qzqdm/dali-dalistyle-mini-parfyum-nov-5-ml.html",
    "https://vendora.bg/items/8jwy1m/pi-givenchy-miniatyuren-parfyum-nov-5ml.html",
    "https://vendora.bg/items/o42nxe/roma-by-laura-biagiotti-miniatyuren-parfyum-nov-za-zheni.html",
    "https://vendora.bg/items/ngxg2q/parfyum-rubylips-dali-miniature-35-ml-nov-plen.html",
    "https://vendora.bg/items/qxjdg2/andy-warhol-miniature-perfume-nov-5-ml.html",
    "https://vendora.bg/items/4qzyoe/pink-wish-chopard-miniatyuren-parfyum-nov.html",
    "https://vendora.bg/items/m3qjqo/salvator-dali-mini-parfyum-nov-5-ml.html",
    "https://vendora.bg/items/ypmj0n/la-perla-morris-mini-parfyum-nov-vintidzh-1987.html",
    "https://vendora.bg/items/4qz4gz/boucheron-pour-homme-eau-de-toilette-5ml-novo-vintidzh.html",
    "https://vendora.bg/items/epkq0k/ferre-by-ferre-miniature-splash-5ml-nov-plen.html",
    "https://vendora.bg/items/d1mq71/miniatyuren-beautiful-estee-lauder-parfyum-nov-35-ml.html",
    "https://vendora.bg/items/pq0991/mimmina-intercosma-miniatyuren-parfyum-nov-vintidzh-5-ml-plen.html",
    "https://vendora.bg/items/2gj3wy/pupa-plumes-parfyum-miniatyura-nov-4-ml.html",
    "https://vendora.bg/items/5xz4nm/miniatyurni-parfyumi-novi-avtentichni-plni-ot-lichna-kolekciya.html",
    "https://vendora.bg/items/ep8omk/kolekciya-ot-vintidzh-miniatyurni-parfyumi-kato-novi-s-originalni-kutii.html",
    "https://vendora.bg/items/ep8o1k/miniatyuri-parfyumi-moschino-novi-vsichki-plni.html",
    "https://vendora.bg/items/k8z5j1/miniatyuren-parfyum-ariana-grande-nov.html",
    "https://vendora.bg/items/pqymkd/parfyum-l-eau-disney-pour-homme-15-ml-nov.html",
    "https://vendora.bg/items/9yzknn/mini-parfyum-ariana-grande-nov-75-ml.html",
    "https://vendora.bg/items/joqwd8/miniatyuren-parfyum-ariana-grande-nov-75-ml.html",
    "https://vendora.bg/items/705wnx/parfyum-miniature-sky-ot-anna-sui-5ml-nov.html",

    # Page 6 (6 URLs)
    "https://vendora.bg/items/4qp27w/miniatyurni-parfyumi-novi-v-otlichno-sstoyanie.html",
    "https://vendora.bg/items/2gqe45/miniatyuren-parfyum-ariana-grande-nov-75-ml.html",
    "https://vendora.bg/items/yp440d/vintidzh-miniatyurni-parfyumi-kato-novi.html",
    "https://vendora.bg/items/34xxgj/vintidzh-miniatyuri-na-parfyumi-kato-novi.html",
    "https://vendora.bg/items/zwqq33/parfyum-mcm-miniature-nov-limited-edition-7ml.html",
    "https://vendora.bg/items/5xzw06/parfyum-christina-aguilera-15ml-nov.html",
]

print(f"Total URLs scraped: {len(all_urls)}")

# Load existing products
try:
    with open('products.json', 'r') as f:
        products = json.load(f)
    print(f"Existing products in products.json: {len(products)}")

    # Extract existing item IDs from vendoraUrls
    existing_item_ids = set()
    for product in products:
        if 'vendoraUrl' in product:
            url = product['vendoraUrl']
            # Extract item ID from URL
            # Format: https://vendora.bg/l/XXXXXXX or https://vendora.bg/items/XXXXXXX/...
            if '/l/' in url:
                item_id = url.split('/l/')[-1]
            elif '/items/' in url:
                item_id = url.split('/items/')[-1].split('/')[0]
            else:
                continue
            existing_item_ids.add(item_id)

    print(f"Unique existing item IDs: {len(existing_item_ids)}")

except FileNotFoundError:
    print("products.json not found, treating all URLs as new")
    existing_item_ids = set()

# Filter out existing URLs by comparing item IDs
new_urls = []
for url in all_urls:
    # Extract item ID from scraped URL
    if '/items/' in url:
        item_id = url.split('/items/')[-1].split('/')[0]
        if item_id not in existing_item_ids:
            new_urls.append(url)
    else:
        # If we can't extract item ID, include it as new
        new_urls.append(url)

print(f"New URLs to scrape: {len(new_urls)}")

# Save new URLs to file
if new_urls:
    with open('urls.txt', 'w') as f:
        for url in new_urls:
            f.write(url + '\n')
    print(f"\nSaved {len(new_urls)} new URLs to urls.txt")
    print("\nNext step: Run 'python sync-vendora.py --urls urls.txt' to fetch and add these products")
else:
    print("\nNo new URLs to scrape - all products are already in products.json!")
