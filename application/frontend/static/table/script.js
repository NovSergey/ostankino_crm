export function openModalEmployee(entry, object_name=null) {
    document.body.classList.add('modal-open');
    document.getElementById("modal-employee").style.display = "block";

    document.getElementById("modalIdLogEmployee").textContent = entry.id;
    document.getElementById("modalLogObjectEmployee").textContent = object_name ? object_name : ( entry.object ? entry.object.name : "-") ;
    document.getElementById("modalEntryTimeEmployee").textContent = entry.entry_time;
    document.getElementById("modalExitTimeEmployee").textContent = entry.exit_time ? entry.exit_time: "-";
    
    document.getElementById("modalIdEmployee").textContent = entry.employee.id;
    document.getElementById("modalIdEmployee").setAttribute("href", "/employees/"+entry.employee.id)
    document.getElementById("modalNameEmployee").textContent = entry.employee.full_name;
    document.getElementById("modalPhoneEmployee").textContent = entry.employee.phone;
    document.getElementById("modalObjectEmployee").textContent = entry.employee.object ? entry.employee.object.name : "Не установлено";
    document.getElementById("modalGroupEmployee").textContent = entry.employee.group ? entry.employee.group.title : "Не установлено";
    document.getElementById("modalSanitaryTableEmployee").textContent = entry.employee.sanitary_table ? entry.employee.sanitary_table.label : "Не установлено";

    
    document.getElementById("modalIdScanerEmployee").textContent = entry.scanned_by_user.id;
    document.getElementById("modalIdScanerEmployee").setAttribute("href", "/employees/"+entry.scanned_by_user.id)
    document.getElementById("modalNameScanerEmployee").textContent = entry.scanned_by_user.full_name;
    document.getElementById("modalPhoneScanerEmployee").textContent = entry.scanned_by_user.phone;
}

export function openModalSecurity(entry, object_name=null) {
    document.body.classList.add('modal-open');
    document.getElementById("modal-security").style.display = "block";

    document.getElementById("modalIdLogSecurity").textContent = entry.id;
    document.getElementById("modalLogObjectSecurity").textContent = object_name ? object_name : ( entry.object ? entry.object.name : "-") ;
    document.getElementById("modalEntryTimeSecurity").textContent = entry.entry_time;
    document.getElementById("modalExitTimeSecurity").textContent = entry.exit_time ? entry.exit_time: "-";
    
    document.getElementById("modalIdSecurity").textContent = entry.employee.id;    
    document.getElementById("modalIdSecurity").setAttribute("href", "/employees/"+entry.employee.id)
    document.getElementById("modalNameSecurity").textContent = entry.employee.full_name;
    document.getElementById("modalPhoneSecurity").textContent = entry.employee.phone;
    document.getElementById("modalObjectSecurity").textContent = entry.employee.object ? entry.employee.object.name : "Не установлено";
    document.getElementById("modalGroupSecurity").textContent = entry.employee.group ? entry.employee.group.title : "Не установлено";
}


function closeModal() {
    document.body.classList.remove('modal-open');
    document.getElementById("modal-employee").style.display = "none";
    document.getElementById("modal-security").style.display = "none";
}

window.closeModal = closeModal;