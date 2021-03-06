#  LLEPE: Liquid-Liquid Equilibrium Parameter Estimator
#  Copyright (C) 2020, UChicago Argonne, LLC. All rights reserved.
#  Released under the modified BSD license. See LICENSE for more details.
import numpy as np
import pandas as pd


def lmse_perturbed_obj(predicted_dict,
                       measured_df,
                       species_list,
                       epsilon=1e-100):
    meas_aq = np.concatenate([measured_df['{0}_aq_eq'.format(species)].values
                              for species in species_list])
    pred_aq = np.concatenate([
        predicted_dict['{0}_aq_eq'.format(species)]
        for species in species_list])

    meas_d = np.concatenate([measured_df['{0}_d_eq'.format(species)].values
                             for species in species_list])
    pred_d = np.concatenate([
        predicted_dict['{0}_d_eq'.format(species)]
        for species in species_list])

    meas_org = meas_aq * meas_d
    pred_org = np.concatenate([
        predicted_dict['{0}_org_eq'.format(species)]
        for species in species_list])

    perturbed_pred_d = (pred_org + epsilon) / (pred_aq + epsilon)
    perturbed_meas_d = (meas_org + epsilon) / (meas_aq + epsilon)
    log_pred_d = np.log10(perturbed_pred_d)
    log_meas_d = np.log10(perturbed_meas_d)

    fun4 = (log_meas_d - log_pred_d) ** 2
    obj = np.mean(fun4)
    return obj


def ind_lmse_perturbed_obj(predicted_dict,
                           measured_df,
                           species_list,
                           epsilon=1e-100):
    pred_df = pd.DataFrame(predicted_dict)
    objectives = []
    for i in range(len(pred_df)):
        pred_aq = pred_df[['{0}_aq_eq'.format(species)
                           for species in species_list]].values[i]
        pred_org = pred_df[['{0}_org_eq'.format(species)
                            for species in species_list]].values[i]
        meas_aq = measured_df[['{0}_aq_eq'.format(species)
                               for species in species_list]].values[i]
        meas_d = measured_df[['{0}_d_eq'.format(species)
                              for species in species_list]].values[i]
        meas_org = meas_aq * meas_d
        perturbed_pred_d = (pred_org + epsilon) / (pred_aq + epsilon)
        perturbed_meas_d = (meas_org + epsilon) / (meas_aq + epsilon)
        log_pred_d = np.log10(perturbed_pred_d)
        log_meas_d = np.log10(perturbed_meas_d)
        fun1 = (log_meas_d - log_pred_d) ** 2
        objectives.append(np.mean(fun1))
    objectives = np.array(objectives)
    return objectives


def mean_squared_error(predicted_dict,
                       measured_df,
                       species_list):
    meas_aq = np.concatenate([measured_df['{0}_aq_eq'.format(species)].values
                              for species in species_list])
    pred_aq = np.concatenate([
        predicted_dict['{0}_aq_eq'.format(species)]
        for species in species_list])

    meas_d = np.concatenate([measured_df['{0}_d_eq'.format(species)].values
                             for species in species_list])
    pred_d = np.concatenate([
        predicted_dict['{0}_d_eq'.format(species)]
        for species in species_list])

    meas_org = meas_aq * meas_d
    pred_org = np.concatenate([
        predicted_dict['{0}_org_eq'.format(species)]
        for species in species_list])
    aq_obj = (meas_aq - pred_aq)**2
    org_obj = (meas_org - pred_org)**2
    objs = np.concatenate([aq_obj, org_obj])
    obj = np.mean(objs)
    return obj
