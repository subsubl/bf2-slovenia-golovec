
Remove Duplicate Textures
=========================

:Original Author: [R-DEV] Arab

The v1.6.3.3 patch introduced a potential 'texture not found' error during model import in windowed mode. I am reducing duplicate textures to optimize Project Reality.

The following textures are identical in v1.6.3.2:

.. code-block:: text

   The following textures are the same:
   common\sky\skydome\textures\cloud01.dds
   common\textures\cloud\cloud01.dds

   The following textures are the same:
   common\sky\skydome\textures\specularlut_pow36.dds
   common\textures\specularlut_pow36.dds
   objects\vehicles\common\textures\specularlut_pow36.dds

   The following textures are the same:
   common\terrain\textures\color\grass.dds
   objects\staticobjects\pr\trench\textures\grass_sb.dds

   The following textures are the same:
   menu\hud\texture\ingame\flags\icons\minimap\arf\minimap_flag.dds
   menu\hud\texture\ingame\flags\icons\minimap\ch\minimap_flag.dds
   menu\hud\texture\ingame\flags\icons\minimap\fr\minimap_flag.dds
   menu\hud\texture\ingame\flags\icons\minimap\us\minimap_flag.dds
   menu\hud\texture\ingame\flags\icons\minimap\usa\minimap_flag.dds
   menu\hud\texture\ingame\flags\icons\minimap\vnusa\minimap_flag.dds
   menu\hud\texture\ingame\flags\icons\minimap\vnusmc\minimap_flag.dds
   menu\hud\texture\ingame\flags\icons\minimap\ww2usa\minimap_flag.dds

   The following textures are the same:
   menu\hud\texture\ingame\flags\icons\minimap\gb\minimap_flag.dds
   menu\hud\texture\ingame\flags\icons\minimap\gb82\minimap_flag.dds

   The following textures are the same:
   menu\hud\texture\ingame\generalicons\ranks\rank_00.dds
   menu\hud\texture\ingame\generalicons\ranks\rank_01.dds
   menu\hud\texture\ingame\generalicons\ranks\rank_02.dds
   menu\hud\texture\ingame\generalicons\ranks\rank_03.dds
   menu\hud\texture\ingame\generalicons\ranks\rank_05.dds
   menu\hud\texture\ingame\generalicons\ranks\rank_06.dds
   menu\hud\texture\ingame\generalicons\ranks\rank_07.dds
   menu\hud\texture\ingame\generalicons\ranks\rank_08.dds
   menu\hud\texture\ingame\generalicons\ranks\rank_09.dds
   menu\hud\texture\ingame\generalicons\ranks\rank_10.dds
   menu\hud\texture\ingame\generalicons\ranks\rank_11.dds
   menu\hud\texture\ingame\generalicons\ranks\rank_12.dds
   menu\hud\texture\ingame\generalicons\ranks\rank_13.dds
   menu\hud\texture\ingame\generalicons\ranks\rank_14.dds
   menu\hud\texture\ingame\generalicons\ranks\rank_15.dds
   menu\hud\texture\ingame\generalicons\ranks\rank_16.dds
   menu\hud\texture\ingame\generalicons\ranks\rank_17.dds
   menu\hud\texture\ingame\generalicons\ranks\rank_18.dds
   menu\hud\texture\ingame\generalicons\ranks\rank_19.dds
   menu\hud\texture\ingame\generalicons\ranks\rank_20.dds
   menu\hud\texture\ingame\generalicons\ranks\rank_21.dds

   The following textures are the same:
   menu\hud\texture\ingame\minimap\icons\icon_supplies.dds
   menu\hud\texture\ingame\minimap\map_commandergrid.dds
   menu\hud\texture\ingame\minimap\map_frame.dds
   menu\hud\texture\ingame\minimap\map_satellitescanline.dds
   menu\hud\texture\ingame\minimap\map_shadow.dds

   The following textures are the same:
   menu\hud\texture\ingame\player\bars\healthbarfull.dds
   menu\hud\texture\ingame\vehicles\bars\armorbarfull.dds

   The following textures are the same:
   menu\hud\texture\ingame\vehicles\icons\hud\air\attack\a10\laserlockbox.dds
   menu\hud\texture\ingame\vehicles\icons\hud\air\attack\ah64a\laserlockbox.dds

   The following textures are the same:
   menu\hud\texture\ingame\vehicles\icons\hud\air\attack\a10\laserlockboxfriendly.dds
   menu\hud\texture\ingame\vehicles\icons\hud\air\attack\ah64a\laserlockboxfriendly.dds

   The following textures are the same:
   menu\hud\texture\ingame\vehicles\icons\hud\air\attack\a10\laserlockboxlocked.dds
   menu\hud\texture\ingame\vehicles\icons\hud\air\attack\ah64a\laserlockboxlocked.dds

   The following textures are the same:
   menu\hud\texture\ingame\vehicles\icons\hud\land\seacat\seacatframe.dds
   menu\hud\texture\ingame\vehicles\icons\hud\sea\type21\cctv_frame.dds

   The following textures are the same:
   menu\nametag\gb\minimap_cp.dds
   menu\nametag\gb82\minimap_cp.dds

   The following textures are the same:
   menu\nametag\gb\minimap_cpbase.dds
   menu\nametag\gb82\minimap_cpbase.dds

   The following textures are the same:
   menu\nametag\us\minimap_cp.dds
   menu\nametag\usa\minimap_cp.dds
   menu\nametag\vnusa\minimap_cp.dds
   menu\nametag\vnusmc\minimap_cp.dds
   menu\nametag\ww2usa\minimap_cp.dds

   The following textures are the same:
   menu\nametag\us\minimap_cpbase.dds
   menu\nametag\usa\minimap_cpbase.dds
   menu\nametag\vnusa\minimap_cpbase.dds
   menu\nametag\vnusmc\minimap_cpbase.dds
   menu\nametag\ww2usa\minimap_cpbase.dds

   The following textures are the same:
   objects\common\ammo_drop_insurgent\textures\ammo_drop_insurgent_b.dds
   objects\common\ammo_drop_ww2ger\textures\ammo_drop_ww2_ger_b.dds

   The following textures are the same:
   objects\common\flags\textures\prflags_b.dds
   objects\staticobjects\common\textures\flags_b.dds

   The following textures are the same:
   objects\common\textures\dummyblack.dds
   objects\vehicles\common\textures\dummyblack.dds

   The following textures are the same:
   objects\common\textures\dummyblack_tis.dds
   objects\vehicles\common\textures\dummyblack_tis.dds

   The following textures are the same:
   objects\common\textures\dummynormal.dds
   objects\vehicles\common\textures\dummynormal.dds

   The following textures are the same:
   objects\common\textures\heliblur\4blatt_ectiger.dds
   objects\vehicles\air\us_ahe_ah1z\textures\us_ahe_ah1z_rotor_c.dds
   objects\vehicles\common\textures\heliblur\4blatt_ectiger.dds

   The following textures are the same:
   objects\common\textures\shadowdefault.dds
   objects\vehicles\common\textures\shadowdefault.dds

   The following textures are the same:
   objects\develop\cube\textures\cube_b.dds
   objects\develop\soundhouse\textures\soundhouse_b.dds

   The following textures are the same:
   objects\develop\cube\textures\cube_c.dds
   objects\develop\cube\textures\cube_de.dds
   objects\develop\soundhouse\textures\soundhouse_c.dds

   The following textures are the same:
   objects\develop\cube\textures\specularlut_pow36.dds
   objects\develop\soundhouse\textures\specularlut_pow36.dds
   objects\develop\woodboard1m\textures\specularlut_pow36.dds
   objects\develop\woodboard2m\textures\specularlut_pow36.dds
   objects\miscobjects\middle-east\gate\textures\specularlut_pow36.dds

   The following textures are the same:
   objects\develop\woodboard1m\textures\housetext_b.dds
   objects\develop\woodboard2m\textures\housetext_b.dds

   The following textures are the same:
   objects\develop\woodboard1m\textures\housetext_c.dds
   objects\develop\woodboard2m\textures\housetext_c.dds
   objects\dynamicobjects\barrels_stacked\textures\housetext_c.dds

   The following textures are the same:
   objects\dynamicobjects\mobileradar_dest\textures\mobileradar_b.dds
   objects\staticobjects\military\buildings\mobileradar_us_dest\textures\mobileradar_b.dds

   The following textures are the same:
   objects\effects\geometry\textures\p_wreck_burntwood_b.dds
   objects\staticobjects\common\roads\wooden_bridge_segment\p_wreck_burntwood_b.dds

   The following textures are the same:
   objects\effects\geometry\wreckparticles\p_wreck_v22\textures\us_the_mv22_b.dds
   objects\vehicles\air\us_the_mv22\textures\us_the_mv22_b.dds

   The following textures are the same:
   objects\effects\textures\anim_muzzleflash_round3p.dds
   objects\effects\textures\animated\anim_muzzleflash_round3p.dds

   The following textures are the same:
   objects\effects\textures\fulldirtblast.dds
   objects\effects\textures\fulldirtblastflip.dds

   The following textures are the same:
   objects\effects\textures\fulldustground.dds
   objects\effects\textures\fulldustground2.dds

   The following textures are the same:
   objects\effects\textures\singles\woodsplinter.dds
   objects\effects\textures\woodsplinter\woodsplinter.dds

   The following textures are the same:
   objects\effects\weapons\tracers\geometry\textures\tracer_mg.dds
   objects\effects\weapons\tracers\geometry\textures\tracer_mg_rev.dds

   The following textures are the same:
   objects\kits\meinsurgent\textures\meinsurgent_kits_civilian_c.dds
   objects\staticobjects\pr\textures\militiaback\null_c.dds
   objects\staticobjects\pr\textures\null_c.dds
   objects\vegitation\pr\textures\null_c.dds

   The following textures are the same:
   objects\miscobjects\common\textures\common_01_c.dds
   objects\miscobjects\common\textures\common_01_de.dds
   objects\staticobjects\common\textures\common_01_de.dds
   objects\staticobjects\textures\common_01_c.dds
   objects\staticobjects\textures\common_01_de.dds

   The following textures are the same:
   objects\miscobjects\common\textures\common_01_deb.dds
   objects\staticobjects\common\textures\common_01_deb.dds
   objects\staticobjects\textures\common_01_deb.dds

   The following textures are the same:
   objects\miscobjects\eod_dory1\textures\wood_c.dds
   objects\staticobjects\pr\textures\wood_c.dds
   objects\staticobjects\textures\wood_c.dds

   The following textures are the same:
   objects\miscobjects\eod_sampan_static\texture\sampan1_b.dds
   objects\miscobjects\eod_sampan2_static\textures\sampan2_b.dds
   objects\miscobjects\eod_sampan3_static\textures\sampan3_b.dds

   The following textures are the same:
   objects\roads\textures\cityroad_c.dds
   objects\staticobjects\common\roads\textures\cityroad_c.dds

   The following textures are the same:
   objects\roads\textures\cityroad_deb.dds
   objects\staticobjects\common\textures\cityroad_deb.dds

   The following textures are the same:
   objects\roads\textures\explosion_mark_xpack21.dds
   objects\roads\textures\explosion_mark_xpack44.dds

   The following textures are the same:
   objects\roads\textures\industrial_arrow.dds
   objects\roads\textures\industrial_arrow2.dds

   The following textures are the same:
   objects\roads\textures\oman_tarmac_overlay.dds
   objects\roads\textures\qinling_tarmac_overlay.dds

   The following textures are the same:
   objects\roads\textures\parkinglots.dds
   objects\roads\textures\parkinglots_dark.dds

   The following textures are the same:
   objects\roads\textures\tarmac_intersectionb.dds
   objects\roads\textures\tarmac_mirrorb.dds

   The following textures are the same:
   objects\soldiers\pr_arg82\textures\arg82_head_05_b_os.dds
   objects\soldiers\pr_mec\textures\mec_head_05_b_os.dds

   The following textures are the same:
   objects\soldiers\pr_arg82\textures\arg82_head_06_b_os.dds
   objects\soldiers\pr_arg82\textures\arg82_head_08_b_os.dds
   objects\soldiers\pr_mec\textures\mec_head_06_b_os.dds
   objects\soldiers\pr_mec\textures\mec_head_08_b_os.dds

   The following textures are the same:
   objects\soldiers\pr_arg82\textures\arg82_head_07_b_os.dds
   objects\soldiers\pr_mec\textures\mec_head_07_b_os.dds

   The following textures are the same:
   objects\soldiers\pr_cf\textures\1p_cf_body_heavy_c_woodland.dds
   objects\soldiers\pr_cf\textures\1p_cf_body_light_c_woodland.dds

   The following textures are the same:
   objects\soldiers\pr_cf\textures\3p_cf_body_heavy_c_snow.dds
   objects\soldiers\pr_cf\textures\3p_cf_body_heavy2_c_snow.dds

   The following textures are the same:
   objects\soldiers\pr_ch\textures\ch_head_01_c.dds
   objects\soldiers\pr_vnnva\textures\nva_head_01_c.dds

   The following textures are the same:
   objects\soldiers\pr_ch\textures\ch_head_02_c.dds
   objects\soldiers\pr_vnnva\textures\nva_head_02_c.dds

   The following textures are the same:
   objects\soldiers\pr_ch\textures\ch_head_03_c.dds
   objects\soldiers\pr_vnnva\textures\nva_head_03_c.dds

   The following textures are the same:
   objects\soldiers\pr_ch\textures\ch_head_04_c.dds
   objects\soldiers\pr_vnnva\textures\nva_head_04_c.dds

   The following textures are the same:
   objects\soldiers\pr_ch\textures\ch_head_05_c.dds
   objects\soldiers\pr_vnnva\textures\nva_head_05_c.dds

   The following textures are the same:
   objects\soldiers\pr_ch\textures\ch_head_06_c.dds
   objects\soldiers\pr_vnnva\textures\nva_head_06_c.dds

   The following textures are the same:
   objects\soldiers\pr_chinsurgent\textures\chinsurgentlthead_b_os.dds
   objects\soldiers\pr_ru\textures\rulthead_b_os.dds

   The following textures are the same:
   objects\soldiers\pr_fr\textures\1p_frbody_b_os.dds
   objects\soldiers\pr_un\textures\1p_eubody_b_os.dds

   The following textures are the same:
   objects\soldiers\pr_fsa\textures\1p_fsa_body_lt_c.dds
   objects\soldiers\pr_meinsurgent\textures\1p_meinsurgent_body_lt_c.dds

   The following textures are the same:
   objects\soldiers\pr_ger\textures\1p_ger_body_c_snow.dds
   objects\soldiers\pr_ger\textures\1p_gerbody_c_snow.dds

   The following textures are the same:
   objects\soldiers\pr_ger\textures\gerheadb_b_os.dds
   objects\soldiers\pr_vnusa\textures\usa_head5_b_os.dds

   The following textures are the same:
   objects\soldiers\pr_hamas\textures\1p_hamas2_body_lt_c.dds
   objects\soldiers\pr_hamas\textures\1p_hamas3_body_c.dds

   The following textures are the same:
   objects\soldiers\pr_idf\textures\1p_idf_body_hv_b_os.dds
   objects\soldiers\pr_meinsurgent\textures\1p_meinsurgent_body_hv_b_os.dds

   The following textures are the same:
   objects\soldiers\pr_idf\textures\idf_head_1_b_os.dds
   objects\soldiers\pr_meinsurgent\textures\meinsurgent_head_heavy_b_os.dds

   The following textures are the same:
   objects\soldiers\pr_mec\textures\1p_mec_body_light_c_sbeneh.dds
   objects\soldiers\pr_mec\textures\1p_mec_body_light4_c_sbeneh.dds

   The following textures are the same:
   objects\soldiers\pr_mec\textures\mec_head_08_c.dds
   objects\soldiers\pr_taliban\textures\taliban_head_heavy_c.dds

   The following textures are the same:
   objects\soldiers\pr_nl\textures\1p_nl_body_c_snow.dds
   objects\soldiers\pr_nl\textures\1p_nl_body_heavy_c_snow.dds

   The following textures are the same:
   objects\soldiers\pr_nl\textures\nl_head5_c.dds
   objects\soldiers\pr_pl\textures\pl_head_heavy1_c.dds

   The following textures are the same:
   objects\soldiers\pr_nl\textures\nl_head6_b_os.dds
   objects\soldiers\pr_us\textures\head03_b_os.dds

   The following textures are the same:
   objects\soldiers\pr_pl\textures\pl_head_heavy3_c.dds
   objects\soldiers\pr_us\textures\uslthead5_c.dds

   The following textures are the same:
   objects\soldiers\pr_ru\textures\1p_ru_body_c_snow.dds
   objects\soldiers\pr_ru\textures\1p_ru3_ltbod_c_snow.dds

   The following textures are the same:
   objects\soldiers\pr_ru\textures\ru3ltbod_c.dds
   objects\soldiers\pr_ru\textures\ru5ltbod_c.dds

   The following textures are the same:
   objects\soldiers\pr_ru\textures\ru3ltbod_c_snow.dds
   objects\soldiers\pr_ru\textures\ru5ltbod_c_snow.dds

   The following textures are the same:
   objects\soldiers\pr_ru\textures\rultbod_2_c.dds
   objects\soldiers\pr_ru\textures\rultbod_c.dds

   The following textures are the same:
   objects\soldiers\pr_ru\textures\rultbod_2_c_snow.dds
   objects\soldiers\pr_ru\textures\rultbod_c_snow.dds

   The following textures are the same:
   objects\soldiers\pr_taliban\textures\taliban_bodciv_c.dds
   objects\soldiers\pr_taliban\textures\taliban_bodlt_c.dds

   The following textures are the same:
   objects\soldiers\pr_taliban\textures\taliban_bodlt_2_b_os.dds
   objects\soldiers\pr_taliban\textures\taliban_bodlt_b_os.dds

   The following textures are the same:
   objects\soldiers\pr_usa\textures\1p_usa_body_heavy_c_snow.dds
   objects\soldiers\pr_usa\textures\1p_usa5_body_c_snow.dds

   The following textures are the same:
   objects\soldiers\pr_usa\textures\usa_3p_heavy_c_snow.dds
   objects\soldiers\pr_usa\textures\usaltbod5_c_snow.dds

   The following textures are the same:
   objects\soldiers\pr_vnusa\textures\usa_head2_b_os.dds
   objects\soldiers\pr_vnusa\textures\usa_head7_b_os.dds
   objects\soldiers\pr_ww2usa\textures\usa_head_01_b_os.dds

   The following textures are the same:
   objects\soldiers\pr_vnusa\textures\usa_head3_b_os.dds
   objects\soldiers\pr_ww2usa\textures\usa_head_02_b_os.dds

   The following textures are the same:
   objects\soldiers\pr_ww2ger\textures\1p_ger_arms_officer_c.dds
   objects\soldiers\pr_ww2ger\textures\1p_ger_arms_soldier23_c.dds

   The following textures are the same:
   objects\soldiers\pr_ww2ger\textures\3p_ger_officer_c.dds
   objects\soldiers\pr_ww2ger\textures\3p_ger_soldier23_c.dds

   The following textures are the same:
   objects\staticobjects\_asia\village\textures\chvillage_01_c.dds
   objects\staticobjects\courtyard\textures\courtyard_01_c.dds

   The following textures are the same:
   objects\staticobjects\_asia\village\textures\chvillage_01_de.dds
   objects\staticobjects\courtyard\textures\courtyard_01_de.dds

   The following textures are the same:
   objects\staticobjects\_asia\village\textures\chvillage_01_deb.dds
   objects\staticobjects\courtyard\textures\courtyard_01_deb.dds

   The following textures are the same:
   objects\staticobjects\_asia\village\textures\chvillage_01_di.dds
   objects\staticobjects\courtyard\textures\courtyard_01_di.dds

   The following textures are the same:
   objects\staticobjects\_asia\village\textures\chvillage_02_de.dds
   objects\staticobjects\courtyard\textures\courtyard_02_de.dds

   The following textures are the same:
   objects\staticobjects\_asia\village\textures\chvillage_02_deb.dds
   objects\staticobjects\courtyard\textures\courtyard_02_deb.dds

   The following textures are the same:
   objects\staticobjects\_asia\village\textures\chvillage_03_de.dds
   objects\staticobjects\pr\textures\chvillage_04_de.dds

   The following textures are the same:
   objects\staticobjects\_asia\village\textures\chvillage_03_deb.dds
   objects\staticobjects\pr\textures\chvillage_04_deb.dds

   The following textures are the same:
   objects\staticobjects\_asia\village\textures\wall01_de.dds
   objects\staticobjects\pr\textures\militiaback\wall01_de.dds

   The following textures are the same:
   objects\staticobjects\_asia\village\textures\wall01_deb.dds
   objects\staticobjects\pr\textures\militiaback\wall01_deb.dds

   The following textures are the same:
   objects\staticobjects\_asia\village\textures\wall02_de.dds
   objects\staticobjects\pr\textures\militiaback\wall02_de.dds

   The following textures are the same:
   objects\staticobjects\_asia\village\textures\wall02_deb.dds
   objects\staticobjects\pr\textures\militiaback\wall02_deb.dds

   The following textures are the same:
   objects\staticobjects\_middle-east\city\textures\mecity_01_c.dds
   objects\staticobjects\textures\mecity_01_c.dds

   The following textures are the same:
   objects\staticobjects\_oleska\textures\olesko_floor_de.dds
   objects\staticobjects\_oleska\textures\patio_de.dds

   The following textures are the same:
   objects\staticobjects\_oleska\textures\olesko_floor_deb.dds
   objects\staticobjects\_oleska\textures\patio_deb.dds

   The following textures are the same:
   objects\staticobjects\america\textures\xp2_usa_01_c_fw.dds
   objects\staticobjects\america\textures\xp2_usa_01_c_sbeneh.dds

   The following textures are the same:
   objects\staticobjects\ammobox_ger\textures\ammobox_ger_b.dds
   objects\staticobjects\armament\pak40_ammo_box\textures\pak40_ammo_box_b.dds

   The following textures are the same:
   objects\staticobjects\bridges\stonebridge_dest_2\textures\dirty_c.dds
   objects\staticobjects\pr\textures\dirty_c.dds

   The following textures are the same:
   objects\staticobjects\buildings\bunkertp\textures\bunkerconc1_b.dds
   objects\staticobjects\buildings\bunkertp\textures\bunkerconc2_b.dds
   objects\staticobjects\buildings\bunkertp\textures\bunkerdirtback_b.dds

   The following textures are the same:
   objects\staticobjects\buildings\bunkertp\textures\bunkerconc2.dds
   objects\staticobjects\buildings\bunkertp\textures\bunkerdirtback.dds
   objects\staticobjects\buildings\bunkertp\textures\bunkerroof.dds

   The following textures are the same:
   objects\staticobjects\buildings\church\textures\windows_c.dds
   objects\staticobjects\buildings\church\textures\windows_c_woodland.dds

   The following textures are the same:
   objects\staticobjects\buildings\dorf\kapelle\textures\green_aging.dds
   objects\staticobjects\textures\opk_color\algenweiss_kachelbar.dds
   objects\staticobjects\textures\opk_color\green_aging.dds

   The following textures are the same:
   objects\staticobjects\buildings\dorf\kapelle\textures\mvr_schilder_c.dds
   objects\staticobjects\textures\opk_color\mvr_schilder_c.dds

   The following textures are the same:
   objects\staticobjects\buildings\farmhouse\textures\dach03.dds
   objects\staticobjects\textures\opk_kachelbar\dach03.dds

   The following textures are the same:
   objects\staticobjects\buildings\farmhouse\textures\dach03_bu.dds
   objects\staticobjects\textures\opk_kachelbar\dach03_bu.dds

   The following textures are the same:
   objects\staticobjects\buildings\nva_hut3\textures\hut_c.dds
   objects\staticobjects\buildings\nva_hut3\textures\hut_de.dds

   The following textures are the same:
   objects\staticobjects\buildings\ruins\texture\bgf_colorruin_c_sbeneh.dds
   objects\staticobjects\textures\bgf_colorwood_c_sbeneh.dds

   The following textures are the same:
   objects\staticobjects\buildings\textures\bg_lumber1_bs.dds
   objects\staticobjects\textures\bg_lumber1_bs.dds

   The following textures are the same:
   objects\staticobjects\buildings\textures\bg_lumber1_dt.dds
   objects\staticobjects\textures\bg_lumber1_dt.dds

   The following textures are the same:
   objects\staticobjects\buildings\textures\bg_lumber1_dt_n.dds
   objects\staticobjects\textures\bg_lumber1_dt_n.dds

   The following textures are the same:
   objects\staticobjects\buildings\textures\bg2oldwood7_n.dds
   objects\staticobjects\textures\bg2oldwood7_n.dds

   The following textures are the same:
   objects\staticobjects\buildings\textures\bg2shingles2_256_n.dds
   objects\staticobjects\textures\bg2shingles2_256_n.dds

   The following textures are the same:
   objects\staticobjects\buildings\textures\bgf_brickwall16_de_sbeneh.dds
   objects\staticobjects\pr\textures\iraq\iblock_de.dds

   The following textures are the same:
   objects\staticobjects\buildings\textures\bgf_brickwall16_nm_sbeneh.dds
   objects\staticobjects\pr\textures\iraq\iblock_deb.dds

   The following textures are the same:
   objects\staticobjects\buildings\textures\wf_alldoors_nm.dds
   objects\staticobjects\textures\wf_alldoors_nm.dds

   The following textures are the same:
   objects\staticobjects\buildings\textures\wf_colormetal_c.dds
   objects\staticobjects\pr\textures\wf_colormetal_c.dds
   objects\staticobjects\textures\wf_colormetal_c.dds

   The following textures are the same:
   objects\staticobjects\buildings\textures\wf_colorwood_c.dds
   objects\staticobjects\textures\wf_colorwood_c.dds

   The following textures are the same:
   objects\staticobjects\buildings\textures\wf_concrete_wall01_nm.dds
   objects\staticobjects\textures\wf_concrete_wall01_nm.dds

   The following textures are the same:
   objects\staticobjects\buildings\textures\wf_concrete_wall02_nm.dds
   objects\staticobjects\textures\wf_concrete_wall02_nm.dds

   The following textures are the same:
   objects\staticobjects\buildings\textures\wf_concrete01_nm.dds
   objects\staticobjects\textures\wf_concrete01_nm.dds

   The following textures are the same:
   objects\staticobjects\buildings\textures\wf_concrete02_nm.dds
   objects\staticobjects\textures\wf_concrete02_nm.dds

   The following textures are the same:
   objects\staticobjects\buildings\textures\wf_corr_metal02a_nm.dds
   objects\staticobjects\textures\wf_corr_metal02a_nm.dds

   The following textures are the same:
   objects\staticobjects\buildings\textures\wf_metal02_nm.dds
   objects\staticobjects\textures\wf_metal02_nm.dds

   The following textures are the same:
   objects\staticobjects\buildings\textures\wf_planks12_nm.dds
   objects\staticobjects\textures\wf_planks12_nm.dds

   The following textures are the same:
   objects\staticobjects\buildings\textures\wf_planks22a_nm.dds
   objects\staticobjects\textures\wf_planks22a_nm.dds

   The following textures are the same:
   objects\staticobjects\buildings\vietoutpost\textures\observation_hut_b.dds
   objects\staticobjects\buildings\vietoutpost2\textures\observation_hut2_b.dds

   The following textures are the same:
   objects\staticobjects\buildings\vietoutpost2\textures\observation_hut2_c.dds
   objects\staticobjects\buildings\vietoutpost2\textures\observation_hut2_de.dds

   The following textures are the same:
   objects\staticobjects\bunker\r112\textures\r112_cr.dds
   objects\staticobjects\bunker\r600\textures\r600_cr.dds

   The following textures are the same:
   objects\staticobjects\common\jerrycan\textures\wehrmacht_fuel_b.dds
   objects\staticobjects\common\jerrycan\textures\wehrmacht_fuel_winter_b.dds

   The following textures are the same:
   objects\staticobjects\common\jerrycan\textures\wehrmacht_fuel_old_b.dds
   objects\staticobjects\common\jerrycan\textures\wehrmacht_fuel_winter_old_b.dds

   The following textures are the same:
   objects\staticobjects\common\repair_hoist\textures\wf_color_c.dds
   objects\staticobjects\pr\textures\wf_color_c.dds
   objects\staticobjects\textures\wf_color_c.dds

   The following textures are the same:
   objects\staticobjects\common\roads\textures\cityroad_cr.dds
   objects\staticobjects\common\textures\cityroad_cr.dds

   The following textures are the same:
   objects\staticobjects\common\roads\woodsteel_bridge_segment\p_wreck_temp_b.dds
   objects\staticobjects\common\roads\woodsteel_bridge_segment\p_wreck_temp_c.dds

   The following textures are the same:
   objects\staticobjects\common\textures\common_01_c_fw.dds
   objects\staticobjects\common\textures\common_01_c_sbeneh.dds

   The following textures are the same:
   objects\staticobjects\common\textures\common_02_c_fw.dds
   objects\staticobjects\common\textures\common_02_c_sbeneh.dds

   The following textures are the same:
   objects\staticobjects\common\textures\common_window02_b.dds
   objects\staticobjects\common\textures\common_window02_c.dds

   The following textures are the same:
   objects\staticobjects\common\textures\common_window03_b.dds
   objects\staticobjects\common\textures\common_window03_c.dds

   The following textures are the same:
   objects\staticobjects\common\textures\xp1_light_glow_01_deb.dds
   objects\staticobjects\common\textures\xp1_light_glow_02_deb.dds
   objects\staticobjects\common\textures\xp1_light_glow_03_deb.dds
   objects\staticobjects\common\textures\xp1_light_glow_05_deb.dds

   The following textures are the same:
   objects\staticobjects\common\textures\xp1_light_glow_05_c.dds
   objects\staticobjects\common\textures\xp1_light_glow_05_de.dds

   The following textures are the same:
   objects\staticobjects\crates\crate_medic\texture\medic_cr.dds
   objects\staticobjects\textures\medic_cr.dds

   The following textures are the same:
   objects\staticobjects\houses\bg_russianvillagehouse\textures\bg2oldpaint_n.dds
   objects\staticobjects\houses\bg_russianvillagehouse2\textures\bg2oldpaint_n.dds

   The following textures are the same:
   objects\staticobjects\industry\textures\industry_obj_01_de_fw.dds
   objects\staticobjects\industry\textures\industry_obj_01_de_sbeneh.dds

   The following textures are the same:
   objects\staticobjects\industry\uniqueobjects\dam\textures\dam_01_c.dds
   objects\staticobjects\industry\uniqueobjects\urm_dam_upper\textures\dam_01_c.dds

   The following textures are the same:
   objects\staticobjects\industry\uniqueobjects\fishingboat\textures\fboat01c.dds
   objects\staticobjects\textures\fboat01c.dds

   The following textures are the same:
   objects\staticobjects\log\textures\bg2rooftop_bs.dds
   objects\staticobjects\pr\textures\bg2rooftop_bs.dds
   objects\staticobjects\textures\bg2rooftop_bs.dds

   The following textures are the same:
   objects\staticobjects\log\textures\wf_lumber_s_d.dds
   objects\staticobjects\textures\wf_lumber_s_d.dds

   The following textures are the same:
   objects\staticobjects\log\textures\wf_lumber_s_nm.dds
   objects\staticobjects\textures\wf_lumber_s_nm.dds

   The following textures are the same:
   objects\staticobjects\log\textures\wf_woodend_04_d.dds
   objects\staticobjects\textures\wf_woodend_04_d.dds

   The following textures are the same:
   objects\staticobjects\log\textures\wf_woodend_04_nm.dds
   objects\staticobjects\textures\wf_woodend_04_nm.dds

   The following textures are the same:
   objects\staticobjects\military\textures\military_01_de.dds
   objects\staticobjects\pr\containers\container\textures\military_01_de.dds

   The following textures are the same:
   objects\staticobjects\military\textures\military_01_deb.dds
   objects\staticobjects\pr\containers\container\textures\military_01_deb.dds

   The following textures are the same:
   objects\staticobjects\military\uniqueobjects\us_carrier_wasp\textures\hull_deb.dds
   objects\staticobjects\military\uniqueobjects\xp1_us_carrier_wasp\textures\hull_deb.dds

   The following textures are the same:
   objects\staticobjects\pr\textures\afghan_1_c.dds
   objects\staticobjects\pr\textures\houses_dest_beam_c.dds
   objects\staticobjects\pr\textures\null_di.dds
   objects\staticobjects\pr\textures\pr_white_c.dds

   The following textures are the same:
   objects\staticobjects\pr\textures\bark2_sandy.dds
   objects\vegitation\pr\textures\bark2_sandy.dds

   The following textures are the same:
   objects\staticobjects\pr\textures\bgf_colordirt_4_c.dds
   objects\staticobjects\textures\bgf_colordirt_4_c.dds

   The following textures are the same:
   objects\staticobjects\pr\textures\boards_v2_debris_sbeneh.dds
   objects\staticobjects\pr\textures\boards_v3_sbeneh.dds
   objects\staticobjects\pr\textures\houses_dest_trim_sbeneh.dds

   The following textures are the same:
   objects\staticobjects\pr\textures\cliff_c.dds
   objects\vegitation\pr\textures\cliff_c.dds

   The following textures are the same:
   objects\staticobjects\pr\textures\cmdr_bunker_marines.dds
   objects\staticobjects\pr\textures\cmdr_bunker_woodland.dds

   The following textures are the same:
   objects\staticobjects\pr\textures\cmdr_bunker_sand_marines.dds
   objects\staticobjects\pr\textures\cmdr_bunker_sand_woodland.dds

   The following textures are the same:
   objects\staticobjects\pr\textures\concrete_wall_01_c.dds
   objects\staticobjects\textures\concrete_wall_01_c.dds

   The following textures are the same:
   objects\staticobjects\pr\textures\conctile_big_fw.dds
   objects\staticobjects\pr\textures\conctile_big_sbeneh.dds

   The following textures are the same:
   objects\staticobjects\pr\textures\houses_dest_tiles_deb_snow.dds
   objects\staticobjects\vietnam\military\wrecks\air\crashed_dustoff\textures\huey_a_dustoff_b.dds
   objects\vehicles\air\ru_ahe_mi24\textures\ru_ahe_mi24_nose_cap_b.dds
   objects\vehicles\land\gb_trk_logistics\textures\gb_truck_slat_b.dds
   objects\vehicles\land\gb_trk_logistics\textures\gb_truck_windows_b.dds
   objects\vehicles\land\us_apc_aavp7a1\textures\us_apc_aavp7a1_cockpit_b.dds

   The following textures are the same:
   objects\staticobjects\pr\textures\militiaback\blockwall_deb_fw.dds
   objects\staticobjects\pr\textures\militiaback\blockwall_sbeneh.dds

   The following textures are the same:
   objects\staticobjects\pr\textures\militiaback\cementpour.dds
   objects\staticobjects\pr\textures\militiaback\cementpour_fw.dds

   The following textures are the same:
   objects\staticobjects\pr\textures\militiaback\null_crb.dds
   objects\staticobjects\pr\textures\null_crb.dds
   objects\staticobjects\pr\textures\pr_misc_crb.dds

   The following textures are the same:
   objects\staticobjects\pr\textures\militiaback\null_de.dds
   objects\staticobjects\pr\textures\null_de.dds
   objects\vegitation\pr\textures\null_de.dds

   The following textures are the same:
   objects\staticobjects\pr\textures\militiaback\null_deb.dds
   objects\staticobjects\pr\textures\null_deb.dds

   The following textures are the same:
   objects\staticobjects\pr\textures\rocks_c.dds
   objects\vegitation\pr\textures\rocks_c.dds

   The following textures are the same:
   objects\staticobjects\pr\textures\rust01_de.dds
   objects\staticobjects\textures\wf_planks22a_d_sbeneh.dds

   The following textures are the same:
   objects\staticobjects\pr\textures\rust01_deb.dds
   objects\staticobjects\textures\wf_planks22a_nm_sbeneh.dds

   The following textures are the same:
   objects\staticobjects\pr\textures\wood_de.dds
   objects\staticobjects\textures\wood_de.dds

   The following textures are the same:
   objects\staticobjects\pr\textures\wood_deb.dds
   objects\staticobjects\textures\wood_deb.dds

   The following textures are the same:
   objects\staticobjects\textures\bgf_colordirt_2_c.dds
   objects\staticobjects\textures\bgf_hay_c.dds

   The following textures are the same:
   objects\staticobjects\textures\common_20_c.dds
   objects\staticobjects\textures\common_20_de.dds

   The following textures are the same:
   objects\staticobjects\textures\eod_vhouse_c.dds
   objects\staticobjects\textures\eod_vhouse_de.dds

   The following textures are the same:
   objects\staticobjects\textures\lzhueyb_b.dds
   objects\staticobjects\textures\lzhueysan_b.dds

   The following textures are the same:
   objects\staticobjects\textures\opk_kachelbar\bodentextur01.dds
   objects\staticobjects\textures\train\einzeltexturen\bodentextur01.dds

   The following textures are the same:
   objects\staticobjects\textures\opk_kachelbar\bodentextur01_bu.dds
   objects\staticobjects\textures\train\einzeltexturen\bodentextur01_bu.dds

   The following textures are the same:
   objects\staticobjects\textures\opk_kachelbar\bodentextur02.dds
   objects\staticobjects\textures\train\einzeltexturen\bodentextur02.dds

   The following textures are the same:
   objects\staticobjects\textures\opk_kachelbar\bodentextur02_bu.dds
   objects\staticobjects\textures\train\einzeltexturen\bodentextur02_bu.dds

   The following textures are the same:
   objects\staticobjects\textures\opk_kachelbar\dach01.dds
   objects\staticobjects\textures\train\einzeltexturen\dach01.dds

   The following textures are the same:
   objects\staticobjects\textures\opk_kachelbar\dach01_bu.dds
   objects\staticobjects\textures\train\einzeltexturen\dach01_bu.dds

   The following textures are the same:
   objects\staticobjects\textures\opk_kachelbar\holz01.dds
   objects\staticobjects\textures\train\einzeltexturen\holz01.dds

   The following textures are the same:
   objects\staticobjects\textures\opk_kachelbar\holz01_bu.dds
   objects\staticobjects\textures\train\einzeltexturen\holz01_bu.dds

   The following textures are the same:
   objects\staticobjects\textures\opk_kachelbar\holzpanelen01.dds
   objects\staticobjects\textures\train\einzeltexturen\holzpanelen01.dds

   The following textures are the same:
   objects\staticobjects\textures\opk_kachelbar\holzpanelen01_bu.dds
   objects\staticobjects\textures\train\einzeltexturen\holzpanelen01_bu.dds

   The following textures are the same:
   objects\staticobjects\textures\opk_kachelbar\innen01.dds
   objects\staticobjects\textures\train\einzeltexturen\innen01.dds

   The following textures are the same:
   objects\staticobjects\textures\opk_kachelbar\innen01_bu.dds
   objects\staticobjects\textures\train\einzeltexturen\innen01_bu.dds

   The following textures are the same:
   objects\staticobjects\textures\opk_kachelbar\mauer01.dds
   objects\staticobjects\textures\train\einzeltexturen\mauer01.dds

   The following textures are the same:
   objects\staticobjects\textures\opk_kachelbar\mauer01_bu.dds
   objects\staticobjects\textures\train\einzeltexturen\mauer01_bu.dds

   The following textures are the same:
   objects\staticobjects\textures\opk_kachelbar\zaun.dds
   objects\staticobjects\textures\train\einzeltexturen\zaun.dds

   The following textures are the same:
   objects\staticobjects\textures\opk_kachelbar\zaun_bu.dds
   objects\staticobjects\textures\train\einzeltexturen\zaun_bu.dds

   The following textures are the same:
   objects\staticobjects\textures\wf_brick_wall02_d.dds
   objects\staticobjects\walls\textures\bgf_stonewall2_d.dds
   objects\staticobjects\walls\textures\wf_colorconcrete_c.dds

   The following textures are the same:
   objects\staticobjects\textures\wf_brick_wall02_nm.dds
   objects\staticobjects\walls\textures\bgf_stonewall2_nm.dds
   objects\staticobjects\walls\textures\wf_concretewall03_d_grey.dds

   The following textures are the same:
   objects\staticobjects\textures\wf_concrete_wall05_d.dds
   objects\staticobjects\textures\wf_concrete_wall06_d.dds

   The following textures are the same:
   objects\staticobjects\textures\wf_concrete_wall05_nm.dds
   objects\staticobjects\textures\wf_concrete_wall06_nm.dds

   The following textures are the same:
   objects\staticobjects\textures\wf_lightbulb_d.dds
   objects\staticobjects\textures\white.dds

   The following textures are the same:
   objects\staticobjects\textures\wf_metal08_nm.dds
   objects\staticobjects\textures\wf_metal09_nm.dds

   The following textures are the same:
   objects\staticobjects\textures\windows_deb.dds
   objects\vehicles\land\mec_jep_brdm2\textures\oh6_windows_b.dds

   The following textures are the same:
   objects\staticobjects\vehicles\uss_allegiance\textures\ship_de.dds
   objects\staticobjects\vehicles\uss_victory\textures\ship_de.dds

   The following textures are the same:
   objects\staticobjects\vehicles\uss_allegiance\textures\ship_deb.dds
   objects\staticobjects\vehicles\uss_victory\textures\ship_deb.dds

   The following textures are the same:
   objects\staticobjects\vietnam\military\wrecks\air\crashed_slick\textures\eod_huey_windows2_c.dds
   objects\vehicles\common\textures\eod_huey_windows2_c.dds

   The following textures are the same:
   objects\vegitation\america\textures\leaf_xp2_olive01de.dds
   objects\vegitation\middle-east\textures\leaf_meolive01de.dds

   The following textures are the same:
   objects\vegitation\asia\textures\leaf_me_nc_drybush01_lod.dds
   objects\vegitation\middle-east\textures\leaf_me_nc_drybush01_lod.dds

   The following textures are the same:
   objects\vegitation\asia\textures\leaf_ncslybush01de.dds
   objects\vegitation\middle-east\textures\leaf_ncslybush01de.dds

   The following textures are the same:
   objects\vegitation\asia\textures\leaf_ncslybush02de_le.dds
   objects\vegitation\middle-east\textures\leaf_ncslybush02de_le.dds

   The following textures are the same:
   objects\vegitation\asia\textures\nccolor.dds
   objects\vegitation\pr\textures\prcolor.dds

   The following textures are the same:
   objects\vegitation\jungle-pr\textures\jungle_tree_04_lod.dds
   objects\vegitation\jungle-pr\textures\jungle_tree_05_lod.dds

   The following textures are the same:
   objects\vegitation\pr\textures\tree_deciduous_2_f_lod.dds
   objects\vegitation\pr\textures\tree_deciduous_2_f2_lod.dds

   The following textures are the same:
   objects\vegitation\pr\textures\tree_deciduous_lod_top_f.dds
   objects\vegitation\pr\textures\tree_deciduous_lod_top_f2.dds

   The following textures are the same:
   objects\vehicles\air\ch_the_z8\textures\ch_the_z8_tailrotor_c.dds
   objects\vehicles\air\ger_the_nh90\textures\ger_the_nh90_tailrotor_c.dds
   objects\vehicles\air\nl_the_nh90\textures\nl_the_nh90_tailrotor_c.dds

   The following textures are the same:
   objects\vehicles\air\fr_ahe_sa342\textures\fr_ahe_sa342_tailrotor_c.dds
   objects\vehicles\air\mec_the_mi17\textures\mec_the_mi17_tailrotor_blurred_c.dds

   The following textures are the same:
   objects\vehicles\air\ger_the_nh90\textures\ger_the_nh90_rotor_c.dds
   objects\vehicles\air\nl_the_nh90\textures\nl_the_nh90_rotor_c.dds

   The following textures are the same:
   objects\vehicles\air\mec_ahe_mi24\textures\mec_ahe_mi24_nose_cap_c.dds
   objects\vehicles\air\ru_ahe_mi24\textures\ru_ahe_mi24_nose_cap_c.dds

   The following textures are the same:
   objects\vehicles\air\mec_ahe_sa341h\textures\gazelle_armament_b.dds
   objects\weapons\armament\missiles\gazelle_at3_wire\textures\at3_missile_b.dds

   The following textures are the same:
   objects\vehicles\air\mec_ahe_sa341h\textures\gazelle_armament_c.dds
   objects\weapons\armament\missiles\gazelle_at3_wire\textures\at3_missile_c.dds

   The following textures are the same:
   objects\vehicles\air\ru_ahe_mi24\textures\ru_ahe_mi24_glow.dds
   objects\vehicles\air\us_the_mv22\textures\us_the_mv22_glow.dds

   The following textures are the same:
   objects\vehicles\air\ru_the_mi8\textures\ru_the_mi8_c_snow.dds
   objects\vehicles\air\ru_the_mi8\textures\ru_the_mi8_c_woodland.dds

   The following textures are the same:
   objects\vehicles\air\us_the_uh60\textures\us_the_uh60_c_snow.dds
   objects\vehicles\air\us_the_uh60\textures\us_the_uh60_c_woodland.dds

   The following textures are the same:
   objects\vehicles\air\us_the_uh60\textures\us_the_uh60_extras_c_snow.dds
   objects\vehicles\air\us_the_uh60\textures\us_the_uh60_extras_c_woodland.dds

   The following textures are the same:
   objects\vehicles\civilian\civ_jep_car\textures\civ_jep_car_black_wreck_c.dds
   objects\vehicles\civilian\civ_jep_car\textures\civ_jep_car_white_wreck_c.dds

   The following textures are the same:
   objects\vehicles\common\textures\ahe_mi24_glass_b.dds
   objects\vehicles\common\textures\glass_b.dds

   The following textures are the same:
   objects\vehicles\common\textures\ahe_mi24_glass_c.dds
   objects\vehicles\common\textures\glass_c.dds

   The following textures are the same:
   objects\vehicles\common\textures\idf_tracks_02_b.dds
   objects\vehicles\common\textures\idf_tracks_b.dds

   The following textures are the same:
   objects\vehicles\common\textures\idf_tracks_02_c.dds
   objects\vehicles\common\textures\idf_tracks_c.dds

   The following textures are the same:
   objects\vehicles\common\textures\m113_1p_b.dds
   objects\vehicles\land\nl_apc_ypr50\textures\m113_1p_b.dds

   The following textures are the same:
   objects\vehicles\common\textures\m1131p_c.dds
   objects\vehicles\land\nl_apc_ypr50\textures\m113_1p_c.dds

   The following textures are the same:
   objects\vehicles\common\textures\tank_gunner_sight_c.dds
   objects\weapons\stationary\pak36\textures\tank_gunner_sight_c.dds

   The following textures are the same:
   objects\vehicles\common\textures\wreck_idf_c.dds
   objects\vehicles\common\textures\wreck1.dds

   The following textures are the same:
   objects\vehicles\land\cf_jep_gwagon\textures\cf_jep_gwagon_support_int_c.dds
   objects\vehicles\land\nl_jep_gwagon\textures\nl_jep_gwagon_support_int_c.dds

   The following textures are the same:
   objects\vehicles\land\cf_tnk_leo2a6\textures\cf_tnk_leo2a6_currentrole_c.dds
   objects\vehicles\land\ger_tnk_leo2a6\textures\ger_tnk_leo2a6_currentrole_c.dds

   The following textures are the same:
   objects\vehicles\land\cf_tnk_leo2a6\textures\cf_tnk_leo2a6_drivewheel_c.dds
   objects\vehicles\land\ger_tnk_leo2a6\textures\ger_tnk_leo2a6_drivewheel_c.dds

   The following textures are the same:
   objects\vehicles\land\ch_apc_wz551\textures\ch_apc_wz551_30mmturret_c.dds
   objects\vehicles\land\ch_ifv_type86\textures\ch_ifv_type86_30mmturret_c.dds

   The following textures are the same:
   objects\vehicles\land\idf_aav_m163\textures\m163_vulcan_b.dds
   objects\weapons\stationary\aa_m167\textures\vulcan_b.dds

   The following textures are the same:
   objects\vehicles\land\idf_aav_m163\textures\m163_vulcan_c.dds
   objects\weapons\stationary\aa_m167\textures\vulcan_c.dds

   The following textures are the same:
   objects\vehicles\land\idf_jep_hmmwv\textures\idf_humvee_b.dds
   objects\vehicles\land\us_jep_hmmwv\textures\humvee_b.dds

   The following textures are the same:
   objects\vehicles\land\mec_apc_btr80\textures\mec_apc_btr80_b.dds
   objects\vehicles\land\ru_apc_btr80\textures\ru_apc_btr80_b.dds

   The following textures are the same:
   objects\vehicles\land\mec_apc_btr80\textures\mec_apc_btr80_turret_b.dds
   objects\vehicles\land\ru_apc_btr80\textures\ru_apc_btr80_turret_b.dds

   The following textures are the same:
   objects\vehicles\land\mec_apc_btr80\textures\mec_apc_btr80_wheel_b.dds
   objects\vehicles\land\ru_apc_btr80\textures\ru_apc_btr80_wheel_b.dds

   The following textures are the same:
   objects\vehicles\land\mec_apc_btr80\textures\mec_apc_btr80_wheel_c.dds
   objects\vehicles\land\ru_apc_btr80\textures\ru_apc_btr80_wheel_c.dds

   The following textures are the same:
   objects\vehicles\land\mec_apc_btr80\textures\mec_apc_btr80a_turret_b.dds
   objects\vehicles\land\ru_apc_btr80\textures\ru_apc_btr80a_turret_b.dds

   The following textures are the same:
   objects\vehicles\land\mil_ifv_bmp1\textures\mil_ifv_bmp1_tracks_b.dds
   objects\vehicles\land\ru_ifv_bmp2\textures\ru_ifv_bmp2_tracks_b.dds

   The following textures are the same:
   objects\vehicles\land\mil_ifv_bmp1\textures\mil_ifv_bmp1_tracks_c.dds
   objects\vehicles\land\ru_ifv_bmp2\textures\ru_ifv_bmp2_tracks_c.dds

   The following textures are the same:
   objects\vehicles\land\mil_ifv_bmp1\textures\mil_ifv_bmp1_tracks_c_woodland.dds
   objects\vehicles\land\ru_ifv_bmp2\textures\ru_ifv_bmp2_tracks_c_woodland.dds

   The following textures are the same:
   objects\vehicles\land\nl_jep_bushmaster\textures\nl_bushmaster_backstep_b.dds
   objects\vehicles\land\nl_jep_bushmaster\textures\nl_bushmaster_backstep_c.dds

   The following textures are the same:
   objects\vehicles\land\ru_ifv_bmp3\textures\ru_ifv_bmp3_c_snow.dds
   objects\vehicles\land\ru_ifv_bmp3\textures\ru_ifv_bmp3_c_woodland.dds

   The following textures are the same:
   objects\weapons\handheld\cfrif_c7scope\textures\elcan_b.dds
   objects\weapons\handheld\uslmg_m249\textures\elcan_b.dds

   The following textures are the same:
   objects\weapons\handheld\gblat_law66\textures\gbat_law66_b.dds
   objects\weapons\handheld\idflat_m72\textures\idflat_m72_b.dds

   The following textures are the same:
   objects\weapons\handheld\gbrif_l1a1\textures\3p_suit_b.dds
   objects\weapons\handheld\rurif_ak74m_1p78\textures\1p78_texture_3p_b.dds
   objects\weapons\handheld\rurif_ak74m_1p78\textures\1p78_texture_b.dds
   objects\weapons\handheld\rurif_ak74mscope\textures\trilux_b.dds

   The following textures are the same:
   objects\weapons\handheld\idfsni_m24\textures\idf_m24_parts_c.dds
   objects\weapons\handheld\ussni_m24\textures\m24_parts_c_snow.dds
   objects\weapons\handheld\ussni_m24\textures\m24_parts_c_woodland.dds

   The following textures are the same:
   objects\weapons\handheld\insrg_rpk\textures\bipod_b.dds
   objects\weapons\handheld\rurif_ak47\textures\bipod_b.dds

   The following textures are the same:
   objects\weapons\handheld\insrg_rpk\textures\bipod_c.dds
   objects\weapons\handheld\rurif_ak47\textures\bipod_c.dds

   The following textures are the same:
   objects\weapons\handheld\insrg_rpk\textures\rpk_b.dds
   objects\weapons\handheld\rurif_ak47\textures\rpk_b.dds

   The following textures are the same:
   objects\weapons\handheld\insrg_rpk\textures\rpk2_b.dds
   objects\weapons\handheld\rurif_ak47\textures\rpk2_b.dds

   The following textures are the same:
   objects\weapons\handheld\klappspaten\textures\shovel_c_snow.dds
   objects\weapons\handheld\klappspaten\textures\shovel_c_woodland.dds

   The following textures are the same:
   objects\weapons\handheld\klappspaten\textures\shovel3p_c_snow.dds
   objects\weapons\handheld\klappspaten\textures\shovel3p_c_woodland.dds

   The following textures are the same:
   objects\weapons\handheld\nlrif_c7nld\textures\c7nld_b.dds
   objects\weapons\handheld\nlrif_c7nldag36\textures\c7nld_b.dds

   The following textures are the same:
   objects\weapons\handheld\nlrif_c7nld\textures\hk416_3p_b.dds
   objects\weapons\handheld\nlrif_c7nldag36\textures\hk416_3p_b.dds

   The following textures are the same:
   objects\weapons\handheld\nlrif_c7nld\textures\hk416_3p_c.dds
   objects\weapons\handheld\nlrif_c7nldag36\textures\hk416_3p_c.dds

   The following textures are the same:
   objects\weapons\handheld\nlrif_c7nld\textures\hk416_3xmag_b.dds
   objects\weapons\handheld\nlrif_c7nldag36\textures\hk416_3xmag_b.dds

   The following textures are the same:
   objects\weapons\handheld\nlrif_c7nld\textures\hk416_3xmag_c.dds
   objects\weapons\handheld\nlrif_c7nldag36\textures\hk416_3xmag_c.dds

   The following textures are the same:
   objects\weapons\handheld\nlrif_c7nld\textures\hk416_3xmagzoom_b.dds
   objects\weapons\handheld\nlrif_c7nldag36\textures\hk416_3xmagzoom_b.dds

   The following textures are the same:
   objects\weapons\handheld\nlrif_c7nld\textures\hk416_3xmagzoom_c.dds
   objects\weapons\handheld\nlrif_c7nldag36\textures\hk416_3xmagzoom_c.dds

   The following textures are the same:
   objects\weapons\handheld\nlrif_c7nld\textures\hk416_b.dds
   objects\weapons\handheld\nlrif_c7nldag36\textures\hk416_b.dds

   The following textures are the same:
   objects\weapons\handheld\nlrif_c7nld\textures\hk416_c.dds
   objects\weapons\handheld\nlrif_c7nldag36\textures\hk416_c.dds

   The following textures are the same:
   objects\weapons\handheld\usrgl_m1garand\textures\m7_he_3p_b.dds
   objects\weapons\handheld\usrgl_m1garand_smoke\textures\m7_smoke_3p_b.dds

   The following textures are the same:
   objects\weapons\handheld\ussni_m24\textures\m24body_c_snow.dds
   objects\weapons\handheld\ussni_m24\textures\m24body_c_woodland.dds

   The following textures are the same:
   objects\weapons\stationary\artillery_m2a1_team2\textures\m2a1_b.dds
   objects\weapons\stationary\lefh105\textures\lefh105_b.dds

   The following textures are the same:
   objects\weapons\stationary\hmg_m2hb\textures\ushmg_m2hb_c.dds
   objects\weapons\stationary\us_m51\textures\us_m51_m2hb_c.dds

   The following textures are the same:
   objects\weapons\stationary\hmg_nsvt\textures\hmg_nsvt_b.dds
   objects\weapons\stationary\hmg_nsvt\textures\hmg_nsvt_c.dds

   The following textures are the same:
   objects\weapons\stationary\zpu4\textures\zpu_4_c_marines.dds
   objects\weapons\stationary\zpu4\textures\zpu_4_c_woodland.dds

To update a texture path, use the :guilabel:`Mesh Shader Wrapper` tool from the Lost Pirate Production toolset.

Drag the mesh file into the program, select :guilabel:`Textures Batch`, double-click the missing texture, and point to the mod folder. Finally, click :guilabel:`Save Mesh`.

The program defaults to the :file:`Documents` folder. Creating a shortcut named :file:`a` pointing to the :file:`mods/pr_edit/objects` folder facilitates faster access.

The filename displays at the bottom of the window. Copy and paste it into the file explorer to locate the texture. Use the texture reference list above to identify the replacement for the missing texture.
